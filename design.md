# Phase 4 design doc by Amirhossein Behzadfar, Abhi Patel, and Kalvin McCallum
___
# Introduction
___
Phase 4 of the network design project implements RDT 3.0 over an unreliable UDP channel with bit-errors and loss. This phase leveraged the mechanisms of phase 3 to ensure that reliable data transfer service is still implemented over the unreliable bit-error prone UDP connection. However, the sender and receiver code has been adjusted to handle two additional scenarios, namely data packet loss and ACK packet loss. The recovery mechanism has also been simplified, as we have implemented a timer. If the correct ACK is not received at the sender by the timer's duration, the sender will resend the data packet to the receiver. Furthermore, a user prompt was added to ensure that the user can easily choose the option and error probability.

# Sender Code
___
![Alt text](imgs/Packet_Class.png?raw=true "Optional Title")
* This snapshot illustrates the packet class created to construct the packets that will be sent to the receiver.
* This class utilizes the make function to construct a package which consists of data, a sequence number, data length, and a checksum.
* Once a packet is less than 1024 bytes, the end of the file has been reached and the bmp file is closed.

![Alt text](imgs/Sender_Class.png?raw=true "Optional Title")
* This snapshot shows the sender class created, with methods to parse packets to the receiver.
* The sender class employs several functions to implement the desired methodologies.
* The rdt receive function is utilized to receive packets from the receiver after a packet has been sent by the sender.
* The corrupt function is utilized to check if the received package is corrupt.
* The rdt send function is used to send packets to the receiver.
* The isAck function is used to check acknowledgements received from the receiver.
* The data_pkt_error function is used to generate data errors in the package sent to the receiver.

![Alt text](imgs/Sender_Main.png?raw=true "Optional Title")
* This screenshot illustrate the main function created to implement the class methods and functions.
* The main function begins by opening the image and begins creating packets by calling the make packet function.
* The main function then utilizes conditional statements to move through the four states of the sender finite state machine.
* A while loop is utilizedto continuously loop through the four states.

# Receiver Code
___
![Alt text](imgs/Receiver_Class_2.png?raw=true "Optional Title")
* This screenshot illustrates the receiver class and functions that were created to receive packets from and send packets to the sender.
* The receiver class employs several functions to implement the desired methodologies.
* The rdt receive function is utilized to receive packets from the sender. 
* The corrupt function is utilized to check if the received package is corrupt. 
* The has_seqnum function is used to determine the sequence number in the package received from the sender.
* The extract function is used to extract the data from the packet sent by the sender.
* The make_packet function is used to contruct the packet that is sent to the sender once a package has been received from the sender.
* The udt send function is used to send packets to the sender after a packet has been received from the sender.

![Alt text](imgs/Receiver_Main_2.png?raw=true "Optional Title")
* This screenshot illustrates the main function that was created to implement the Receiver class methods and functions.
* The main function utilizes conditional statements to move through the two states of the receiver finite state machine.
* A while loop is utilized to continuously loop through the two states.

# Checksum
___
![Alt text](imgs/Checksum.png?raw=true "Optional Title")
* This screenshot illustrates the code that was created to implement the checksum.
* The checksum functions by flipping two bits at a time.
* A unique checksum is generated for each packet that is sent from the sender to the receiver.
* The checksum function is also used to ensure that the correct data content from the sender has been received.

# Sender/Receiver Execution
___
![Alt text](imgs/Sender_Receiver_Execution.png?raw=true "Optional Title")
* This image illustrates the transferred BMP file between a UDP client process and a UDP server process.

# Commandline for Execution Start and End for Sender/Receiver
![Alt text](imgs/P4_ExecutionStart_Sender.jpg?raw=true "Optional Title")
* Commandline for starting sender file execution

![Alt text](imgs/P4_ExecutionEnd_Sender.jpg?raw=true "Optional Title")
* Commandline for finished sender file execution

![Alt text](imgs/P4_ExecutionStart_Receiver.jpg?raw=true "Optional Title")
* Commandline for starting receiver file execution

![Alt text](imgs/P4_ExecutionEnd_Receiver.jpg?raw=true "Optional Title")
* Commandline for finished receiver file execution


#  Plot Illustrating Completion Time For All Five Options  
___
![Alt text](imgs/CompletionTimeGraphPhase4.png?raw=true "Optional Title")
* This image illustrates the completion time for all 5 options for transferring the same file at 0% loss/error to 60% loss/error in increments of 5%.
* Option 1 does not have a curve since it is only run with no errors, for which it had a completion time of about 0.788 seconds
* From the graph, the completion time increases as the error amount rises.
* Options 3, 4 and 5 all have near identical runtime curves as the error amount increases, peaking at just over 60 seconds at 60% error, while option 2 peaked at around 25 seconds at 60% error.


