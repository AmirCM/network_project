# Phase 2 design doc by Amirhossein Behzadfar, Abhi Patel, and Kalvin McCallum
___
Implement RDT 1.0 over a reliable UDP channel. Transfer a BMP file between a UDP client process and a UDP server process. 

# Sender Code
___
![Alt text](imgs/Sender_Class.png?raw=true "Optional Title")
* This snapshot shows the sender class created, with methods to parse the bmp file and close the socket
* Class contains attributes for the serverport, server name, socket, and packet array
* make_packet() method opens the bmp file, and reads 1024B packets of the file at a time, storing these packets in an array
* seek() allows for skipping over bytes already read, end of file found when a packet is less than 1024B

![Alt text](imgs/Sender_Main.png?raw=true "Optional Title")
* This screenshot shows the main code written to utilize the class methods/attributes to send packets to the receiver.
* An instance of the class is initialized (server IP address is written where gethostname() is, then the make_packet() function is called
* The file ends with sending each packet one-by-one to the receiver then closing the socket.

# Receiver Code
___
![Alt text](imgs/Receiver_Class.png?raw=true "Optional Title")
* This screenshot illustrates the receiver class that was constructed to receive packets from the sender.
* After receiving the incoming packets, we will store the packets in an array. 
* We will then write the packets to an image file.
* Finally, we will open the bitmap file.

![Alt text](imgs/Receiver_Main.png?raw=true "Optional Title")
* This screenshot illustrates the main function that was created to implement the class methods to receive packets from the sender.
* The bmp file is opened and the make file is utilized.
* The image is then printed.

# Client GUI Code
___
![Alt text](imgs/GUI_Client.png?raw=true "Optional Title")

# Server GUI Code
___
![Alt text](imgs/GUI_Server.png?raw=true "Optional Title")

# Client Code
___
![Alt text](imgs/client_snap.png?raw=true "Optional Title")
* Initiate a UDP socket (SOCK_DGRAM), with the given port that server is listening to and the local host.
* Sending the argument value passed to the code. 
* Receiving the response from the server.

# Server Code
___
![Alt text](imgs/server_snap.png?raw=true "Optional Title")
* Initiate a UDP socket (SOCK_DGRAM), then in a while loop listen to the given port and any host.
* After getting the incoming data, we will send it back to client. 
* In case of getting 'exit' command the loop will break.

# Client/Server Execution
___
![Alt text](imgs/phase_1.png?raw=true "Optional Title")
* This image illustrates the execution of the UDP client server network.

# Sender/Receiver Execution
___
![Alt text](imgs/Sender_Receiver_Execution.png?raw=true "Optional Title")
* This image illustrates the transferred BMP file between a UDP client process and a UDP server process.

# GUI Execution
___
![Alt text](imgs/Server_GUI.png?raw=true "Optional Title")
* Server_GUI Initialized.

![Alt text](imgs/Client_GUI.png?raw=true "Optional Title")
* Client GUI Initialized.

![Alt text](imgs/Client_Image_Selected.png?raw=true "Optional Title")
* Selected BMP file that will be transferred between a UDP client process and a UDP server process.

![Alt text](imgs/Incoming_Image_Received_Server.png?raw=true "Optional Title")
* Incoming image message displayed on Receiver GUI.

![Alt text](imgs/Received_Image_GUI_Server.png?raw=true "Optional Title")
* Image received at Receiver GUI.
