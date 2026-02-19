<div align="center">
  <h1>🌐 Socket Programming with Python</h1>
  <p><b>A Fundamental Implementation of Client-Server Communication via TCP Sockets</b></p>

  <img src="https://img.shields.io/badge/Language-Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Category-Networking-blue?style=for-the-badge" alt="Networking">
</div>

<hr />

## 📖 Overview
This project demonstrates the core principles of **Socket Programming** using Python's built-in `socket` library. It establishes a Transmission Control Protocol (TCP) connection between a Server and a Client, allowing for reliable, connection-oriented data exchange.

Understanding socket communication is a critical pillar in **Cybersecurity**, as it forms the basis for analyzing network traffic, building port scanners, and understanding how malware communicates with Command & Control (C2) servers.



<hr />

## ⚙️ How the Connection Works
The project consists of two main scripts that interact over a local or networked IP address using a specific port.

<table>
  <tr>
    <th>Component</th>
    <th>Role & Logic</th>
  </tr>
  <tr>
    <td><b>Server</b></td>
    <td>Binds to an IP/Port, listens for incoming connections, and accepts requests from the client.</td>
  </tr>
  <tr>
    <td><b>Client</b></td>
    <td>Initiates a connection request to the server's address and sends/receives data.</td>
  </tr>
  <tr>
    <td><b>TCP Socket</b></td>
    <td>Ensures data integrity through error checking and guaranteed delivery of packets.</td>
  </tr>
</table>



<hr />

## 🚀 Getting Started

### Prerequisites
* **Python 3.x** installed on your system.

### Usage
1.  **Clone the repo:**
    ```bash
    git clone https://github.com/5ymb/SocketProgramingWithPython.git
    ```
2.  **Run the Server first:**
    ```bash
    python server.py
    ```
3.  **Run the Client in a separate terminal:**
    ```bash
    python client.py
    ```

<hr />

## 🛠️ Key Concepts & Configuration

### 📡 Network Setup
By default, the code uses `localhost` (127.0.0.1). To test this across two different machines on the same network:
* **Server:** Change the IP in `server.py` to `0.0.0.0` to listen on all available network interfaces.
* **Client:** Change the IP in `client.py` to the **Private IP address** of the Server machine (e.g., `192.168.1.5`).
* **Firewall:** Ensure the chosen Port (e.g., 12345) is allowed through your OS firewall.

### 💻 Code Features
<ul>
  <li><b>Socket Creation:</b> Uses <code>socket.socket(socket.AF_INET, socket.SOCK_STREAM)</code> for IPv4 TCP communication.</li>
  <li><b>Encoding/Decoding:</b> Uses <code>.encode()</code> and <code>.decode()</code> to transform string data into bytes for network transit.</li>
  <li><b>Error Handling:</b> Demonstrates the importance of closing connections to avoid "Address already in use" errors.</li>
</ul>

<hr />

<div align="center">
  <p><i>Developed for Educational Purposes in Network Security and Distributed Systems.</i></p>
  <p><b>Maintained by <a href="https://github.com/5ymb">5ymb</a></b></p>
</div>
