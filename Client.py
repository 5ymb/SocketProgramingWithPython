import tkinter as tk
from tkinter import scrolledtext, simpledialog
import socket
import ssl
import threading
import sys

# --- CONFIGURATION ---
# Change this to your server's IP (the one running Server.py)
HOST = '192.168.56.1'
PORT = 65432
# ---------------------

class SimpleChatClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Chat")
        self.root.geometry("400x450")

        # --- Get Username ---
        self.username = simpledialog.askstring("Username", "Enter your username:", parent=root)
        if not self.username:
            root.destroy()
            sys.exit(0)
            
        self.root.title(f"Chat - {self.username}")

        # --- Create GUI Widgets ---
        
        # Chat display area
        self.chat_area = scrolledtext.ScrolledText(root, state=tk.DISABLED, wrap=tk.WORD, bg="#f0f0f0", font=("Helvetica", 10))
        self.chat_area.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Define styles for messages
        self.chat_area.tag_config('server', foreground='gray', font=("Helvetica", 9, "italic"))
        self.chat_area.tag_config('self', foreground='blue', font=("Helvetica", 10, "bold"))
        self.chat_area.tag_config('other', foreground='black', font=("Helvetica", 10))
        
        # Frame for input and send button
        input_frame = tk.Frame(root)
        input_frame.pack(padx=10, pady=(0, 10), fill=tk.X)
        
        self.msg_entry = tk.Entry(input_frame, font=("Helvetica", 10))
        self.msg_entry.pack(fill=tk.X, expand=True, side=tk.LEFT, padx=(0, 5))
        
        self.send_button = tk.Button(input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)
        
        # Bind <Return> key to send_message
        self.root.bind('<Return>', self.send_message)
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # --- SSL and Socket Setup ---
        self.ssl_sock = None
        self.connect_to_server()

    def connect_to_server(self):
        """Creates the SSL socket and starts the receiver thread."""
        try:
            # 1. Standard socket
            sock = socket.create_connection((HOST, PORT))
            
            # 2. SSL context (for testing, trust any cert)
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            # 3. Wrap socket with SSL
            self.ssl_sock = context.wrap_socket(sock, server_hostname=HOST)
            
            # 4. Send username
            self.ssl_sock.sendall(self.username.encode())
            
            # 5. Start the receiver thread
            # This thread will listen for messages so the GUI doesn't freeze
            self.receiver_thread = threading.Thread(target=self.receive_messages, daemon=True)
            self.receiver_thread.start()
            
            self.display_message("Connected!", "server")
            
        except Exception as e:
            self.display_message(f"Failed to connect: {e}", "server")
            if "certificate" in str(e):
                self.display_message("Tip: Is your cert.pem valid?", "server")
            self.msg_entry.config(state=tk.DISABLED)
            self.send_button.config(state=tk.DISABLED)

    def receive_messages(self):
        """Runs in a separate thread to listen for incoming messages."""
        while True:
            try:
                data = self.ssl_sock.recv(1024)
                if not data:
                    self.display_message("Disconnected from server.", "server")
                    break
                
                # We need to update the GUI from the main thread
                # `after(0, ...)` is a safe way to do this from another thread
                self.root.after(0, self.display_message, data.decode(), "other")
                
            except Exception:
                self.display_message("Connection lost.", "server")
                self.msg_entry.config(state=tk.DISABLED)
                self.send_button.config(state=tk.DISABLED)
                break

    def send_message(self, event=None):
        """Sends a message from the GUI."""
        message = self.msg_entry.get()
        if not message or not self.ssl_sock:
            return
            
        self.msg_entry.delete(0, tk.END)
        
        try:
            self.ssl_sock.sendall(message.encode())
            
            # Display our *own* message immediately
            # We check the format to match the server's broadcast
            if ":" not in message:
                self.display_message(f"{self.username}: {message}", "self")

            if message.lower() == 'exit':
                self.on_closing()
                
        except Exception as e:
            self.display_message(f"Error sending: {e}", "server")

    def display_message(self, message, tag):
        """Safely updates the chat_area widget."""
        self.chat_area.config(state=tk.NORMAL)
        
        # Adjust tag logic for self-display
        if tag == "self":
            self.chat_area.insert(tk.END, f"{message}\n", "self")
        elif tag == "other":
            # Determine if it's a server or user message
            if message.startswith("[SERVER]"):
                self.chat_area.insert(tk.END, f"{message}\n", "server")
            elif ":" in message:
                # Check if this "other" message is actually our own echo
                try:
                    user, _ = message.split(":", 1)
                    if user == self.username:
                        self.chat_area.insert(tk.END, f"{message}\n", "self")
                    else:
                        self.chat_area.insert(tk.END, f"{message}\n", "other")
                except ValueError:
                    self.chat_area.insert(tk.END, f"{message}\n", "other")
            else:
                self.chat_area.insert(tk.END, f"{message}\n", "other")
        elif tag == "server":
             self.chat_area.insert(tk.END, f"{message}\n", "server")
             
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.yview(tk.END) # Auto-scroll

    def on_closing(self):
        """Handles closing the window."""
        if self.ssl_sock:
            try:
                # Send 'exit' one last time
                self.ssl_sock.sendall('exit'.encode())
            except Exception:
                pass # Socket might already be closed
            finally:
                self.ssl_sock.close()
        self.root.destroy()

# --- Main execution ---
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleChatClient(root)
    
    # Only run mainloop if username was provided
    if app.username:
        root.mainloop()
