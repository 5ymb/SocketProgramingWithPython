<div align="center">
  <h1>🌐 Socket Programming with Python</h1>
  <p><b>A Fundamental Implementation of Client-Server Communication via TCP Sockets</b></p>

  <img src="https://img.shields.io/badge/User-5ymb-blueviolet?style=for-the-badge&logo=github" alt="User 5ymb">
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
    git clone [https://github.com/5ymb/SocketProgramingWithPython.git](https://github.com/5ymb/SocketProgramingWithPython.git)
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

## 🛠️ Key Concepts Covered
<ul>
  <li><b>Socket Creation:</b> Using <code>socket.socket()</code> to define the address family (AF_INET) and protocol (SOCK_STREAM).</li>
  <li><b>Bind & Listen:</b> Setting up the server to "wait" on a specific network interface.</li>
  <li><b>Data Encoding:</b> Handling the transformation of string data into bytes for transmission across the network.</li>
  <li><b>Resource Management:</b> Properly closing sockets to prevent port hanging and memory leaks.</li>
</ul>

<hr />

<div align="center">
  <p><i>Developed for Educational Purposes in Network Security and Distributed Systems.</i></p>
  <p><b>Maintained by <a href="https://github.com/5ymb">5ymb</a></b></p>
</div>
