import socket
import ssl
import threading

# --- SSL Setup ---
# Make sure you have 'cert.pem' and 'key.pem' in the same folder
try:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
except FileNotFoundError:
    print("Error: 'cert.pem' or 'key.pem' file not found.")
    print("Please generate them and try again.")
    exit(1)
# ---------------------

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind(('192.168.56.1', 65432)) 
server_sock.listen(5)

print("Secure Chat Server is listening on port 65432...")

clients = []  # List of connected client sockets
clients_lock = threading.Lock()

def broadcast(sender_sock, message):
    """Sends a message to all clients except the sender."""
    with clients_lock:
        # We iterate over a copy of the list in case it's modified
        # during iteration by another thread.
        for client in list(clients):
            if client != sender_sock:
                try:
                    client.sendall(message)
                except (BrokenPipeError, ConnectionResetError):
                    # Client connection is broken, remove them
                    print(f"Broken pipe to client {client.getpeername()}, removing.")
                    clients.remove(client)
                    client.close()
                except Exception as e:
                    print(f"Error broadcasting to client: {e}")
                    clients.remove(client)
                    client.close()

def handle_client(ssl_client_sock, addr):
    """Handles a single client connection."""
    print(f"[+] Client connected from {addr}")
    username = ""
    try:
        # 1. Get username first
        # This is expected by our tkinter client
        username_data = ssl_client_sock.recv(1024)
        if not username_data:
            raise Exception("Client disconnected before sending username")
        
        username = username_data.decode().strip()
        
        # 2. Add client to list *after* getting username
        with clients_lock:
            clients.append(ssl_client_sock)
        
        print(f"[+] Username '{username}' set for {addr}")
        
        # 3. Announce new user to everyone
        join_msg = f"[SERVER] {username} has joined the chat.".encode()
        broadcast(ssl_client_sock, join_msg) # Announce new user

        # 4. Loop for messages
        while True:
            data = ssl_client_sock.recv(1024)
            if not data:
                break  # Client disconnected
            
            message_text = data.decode().strip()

            # 5. Handle 'exit' command
            if message_text.lower() == 'exit':
                break 
            
            # 6. Format and broadcast message
            msg = f"{username}: {message_text}".encode()
            print(f"New message from {username}: {message_text}") # Server console log
            broadcast(ssl_client_sock, msg)
            
    except ConnectionResetError:
        print(f"[-] Client {addr} ({username}) disconnected unexpectedly.")
    except Exception as e:
        print(f"[-] Error with {addr} ({username}): {e}")
    finally:
        # 7. Cleanup
        with clients_lock:
            if ssl_client_sock in clients:
                clients.remove(ssl_client_sock)
        
        if username: # Only broadcast if username was set
            left_msg = f"[SERVER] {username} has left the chat.".encode()
            print(f"[-] Client {addr} ({username}) disconnected")
            broadcast(ssl_client_sock, left_msg) # Announce departure
        else:
            print(f"[-] Client {addr} disconnected before setting username")
            
        ssl_client_sock.close()


# --- Main Server Loop ---
while True:
    try:
        # Wait for a new connection
        client_sock, addr = server_sock.accept()
        
        # Wrap the socket with SSL
        ssl_client_sock = context.wrap_socket(client_sock, server_side=True)

        # Handle this client in a new thread
        # daemon=True means the thread will close when the main program exits
        client_thread = threading.Thread(target=handle_client, 
                                         args=(ssl_client_sock, addr), 
                                         daemon=True)
        client_thread.start()
        
    except Exception as e:
        print(f"[!] Server error in main loop: {e}")
        break # Exit loop on major error

server_sock.close()
print("Server shutting down.")
