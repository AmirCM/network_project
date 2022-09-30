# Phase 2 design doc by Amirhossein Behzadfar, Abhi Patel, and Kalvin McCallum
___
Implement RDT 1.0 over a reliable UDP channel. Transfer a BMP file between a UDP client process and a UDP server process. 

# Server/Receiver code
___
![Alt text](imgs/Receiver_Phase2.png?raw=true "Optional Title")
* Initiate a UDP receiver socket (SOCK_DGRAM) first, then in a while loop listen to the given port and any host.
* After receiving the incoming packets, we will store the packets in an array. 
* We will then write the packets to an image file.
* Finally, we will open the bitmap file.

# Client code
___
![Alt text](imgs/client_snap.png?raw=true "Optional Title")
* Initiate a UDP socket (SOCK_DGRAM), with the given port that server is listening to and the local host.
* Sending the argument value passed to the code. 
* Receiving the response from the server

# Execution
___
![Alt text](imgs/phase_1.png?raw=true "Optional Title")
