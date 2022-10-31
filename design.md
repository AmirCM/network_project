# Phase 3 design doc by Amirhossein Behzadfar, Abhi Patel, and Kalvin McCallum
___
Implementation of RDT 2.2 over a reliable UDP channel. 
Error handling for image file transfer including no loss/bit-errors, ACK packet bit-error, data packet bit-error.

# Sender Code
___
![Alt text](imgs/Sender_Class.png?raw=true "Optional Title")
* This snapshot shows the sender class created, with methods to parse packets to the receiver.
* Class contains attributes for the serverport, server name, socket, and packet array
* make_packet() method opens the bmp file, and reads 1024B packets of the file at a time, storing these packets in an array
* seek() allows for skipping over bytes already read, end of file found when a packet is less than 1024B

![Alt text](imgs/Sender_Main.png?raw=true "Optional Title")
* This screenshot illustrate the main function created to implement the class methods and functions.
* The main function utilizes conditional staements to move through the four states of the sender finite state machine.


# Receiver Code
___
![Alt text](imgs/Receiver_Class.png?raw=true "Optional Title")
* This screenshot illustrates the receiver class and functions that were created to receive packets from and send packets to the sender.

![Alt text](imgs/Receiver_Main.png?raw=true "Optional Title")
* This screenshot illustrates the main function that was created to implement the Receiver class methods and functions.

# Sender/Receiver Execution
___
![Alt text](imgs/Sender_Receiver_Execution.png?raw=true "Optional Title")
* This image illustrates the transferred BMP file between a UDP client process and a UDP server process.

#  Plot Illustrating Completion Time For All Three Options 
___

* This image illustrates the completion time for all 3 options for transferring the same file at 0% loss/error to 60% loss/error in increments of 5%. 


