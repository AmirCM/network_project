# Phase 3 design doc by Amirhossein Behzadfar, Abhi Patel, and Kalvin McCallum
___
Implementation of RDT 2.2 over a reliable UDP channel. 
Error handling for image file transfer including no loss/bit-errors, ACK packet bit-error, data packet bit-error.

# Sender Code
___
![Alt text](imgs/Packet_Class.png?raw=true "Optional Title")
* This snapshot illustrates the packet class created to construct the packets that will be sent to the receiver.
* This class utilizes the make function to construct a package which consists of data, a sequence number, data length, 

![Alt text](imgs/Sender_Class.png?raw=true "Optional Title")
* This snapshot shows the sender class created, with methods to parse packets to the receiver.
* The sender class employs several functions to implement the desired methodologies.
* The functions included in the sender class are as follows:

![Alt text](imgs/Sender_Main.png?raw=true "Optional Title")
* This screenshot illustrate the main function created to implement the class methods and functions.
* The main function utilizes conditional staements to move through the four states of the sender finite state machine.

# Receiver Code
___
![Alt text](imgs/Receiver_Class.png?raw=true "Optional Title")
* This screenshot illustrates the receiver class and functions that were created to receive packets from and send packets to the sender.

![Alt text](imgs/Receiver_Main.png?raw=true "Optional Title")
* This screenshot illustrates the main function that was created to implement the Receiver class methods and functions.

# Checksum
___
![Alt text](imgs/Checksum.png?raw=true "Optional Title")
* This screenshot illustrates the code that was created to implement the checksum.

# Sender/Receiver Execution
___
![Alt text](imgs/Sender_Receiver_Execution.png?raw=true "Optional Title")
* This image illustrates the transferred BMP file between a UDP client process and a UDP server process.

#  Plot Illustrating Completion Time For All Three Options  
___

* This image illustrates the completion time for all 3 options for transferring the same file at 0% loss/error to 60% loss/error in increments of 5%. 


