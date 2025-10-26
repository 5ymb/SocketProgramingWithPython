This application requires you to be on the same LAN to connect to the server to start messaging.
There is a Server.py file that you run on the device you want to make a server. 
And there Client.py, you run it on the client's devices.
You need to create an OpenSSL Certificate and Key, and name them cert.pem and key.pem also put them in the file with the codes(Either Server.py or Client.py).
Client.py also has a GUI, so it is much easier for clients to communicate with each other.
IMPORTANT You have to change the IP to your server IP