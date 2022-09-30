# Phase 2 design doc by Amirhossein Behzadfar, Abhi Patel, and Kalvin McCallum
___
Implement RDT 1.0 over a reliable UDP channel. Transfer a BMP file between a UDP client process and a UDP server process. 

# Sender Code
___
![Alt text](imgs/senderclass_snap.JPG?raw=true "Optional Title")
* This snapshot shows the sender class created, with methods to parse the bmp file and close the socket
* Class contains attributes for the serverport, server name, socket, and packet array
* make_packet() method opens the bmp file, and reads 1024B packets of the file at a time, storing these packets in an array
* seek() allows for skipping over bytes already read, end of file found when a packet is less than 1024B

![Alt text](imgs/sendermain_snap.JPG?raw=true "Optional Title")
* This screenshot shows the code written to utilize the class methods/attributes to send packets to the receiver.
* An instance of the class is initialized, then the make_packet() function is called
* The file ends with sending each packet one-by-one to the receiver then closing the socket.




# Receiver code
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
