# Phase 5 design doc by Amirhossein Behzadfar, Abhi Patel, and Kalvin McCallum
___
# Introduction
___
Phase 5 of the network design project implements Go-Back-N protocol over an unreliable UDP channel with bit-errors and loss. Similar to phase 4, phase 5 implements five data transfer senarios, namely no loss/bit-errors, ack packet bit-errors, data packet bit-error, ack packet loss, and data packet loss. However, data transfer is implemented using a pipelined method. Two primary approaches used to implemented the pipelined protocol include Go-Back-N and selective repeat. In Go-Back-N, the sender transmits multiple packets without waiting for an acknowledgement, but is constrained by a maximum number of unacknowledges packets allowed in the pipeline. The selective repeat protocol ensures that the sender only retransmits the packets that it suspects were received in error by the receiver. Thus, the receiver acknowledges only the individual packets that are received irrespective of the order. 

# Sender Code
___
![Alt text](imgs/Sender_Packet_Class.png?raw=true "Optional Title")
* This snapshot illustrates the packet class created to construct the packets that will be sent to the receiver.
* This class utilizes the make function to construct a package which consists of data, a sequence number, data length, and a checksum.
* Once a packet is less than 1024 bytes, the end of the file has been reached and the bmp file is closed.

![Alt text](imgs/Sender_Class.png?raw=true "Optional Title")
* This snapshot shows the sender class created, with methods to parse packets to the receiver.
* The sender class employs several functions to implement the desired methodologies.
* The rdt receive function is utilized to receive packets from the receiver after a packet has been sent by the sender. An additional conditional is added to this function to remove/ignore the received ACK packet given a loss probability.
* The corrupt function is utilized to check if the received package is corrupt.
* The rdt send function is used to send packets to the receiver.
* The isAck function is used to check acknowledgements received from the receiver.
* The data_pkt_error function is used to generate data errors in the package sent to the receiver.

![Alt text](imgs/Timeout_Func.png?raw=true "Optional Title")
* The timeout function serves as the new recovery mechanism if there are bit-errors or lost packets. The timeout is set to 50 ms.

![Alt text](imgs/Sender_Main.png?raw=true "Optional Title")
* These screenshots illustrate the main function code written to implement the class methods and functions.
* The main function begins by accepting arguments for the option number and error/loss amount.
* The main function then opens the image and begins creating packets by calling the make packet function.
* The main function then utilizes conditional statements to move through the four states of the sender finite state machine. The timeout is now used as the recovery mechanism in the event of errors.
* A while loop is utilized to continuously loop through the four states.

# Receiver Code
___
![Alt text](imgs/Receiver_Class.png?raw=true "Optional Title")
* This screenshot illustrates the receiver class and functions that were created to receive packets from and send packets to the sender.
* The receiver class employs several functions to implement the desired methodologies.
* The rdt receive function is utilized to receive packets from the sender, and a conditional is added in phase 4 to ignore packets based on the input error/loss probability.
* The corrupt function is utilized to check if the received package is corrupt. 
* The has_seqnum function is used to determine the sequence number in the package received from the sender.
* The extract function is used to extract the data from the packet sent by the sender.
* The make_packet function is used to contruct the packet that is sent to the sender once a package has been received from the sender.
* The udt send function is used to send packets to the sender after a packet has been received from the sender.

![Alt text](imgs/Receiver_Main.png?raw=true "Optional Title")
* These screenshots illustrates the main function code written to implement the Receiver class methods and functions.
* First, the main function accepts arguments for the option number and error/loss amount.
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

# Commandline Outputs for Sender/Receiver

# Option 1
![Alt text](imgs/Sender_Option_1.png?raw=true "Optional Title")
* Commandline for sender file execution

![Alt text](imgs/Receiver_Option_1.png?raw=true "Optional Title")
* Commandline for receiver file execution

# Option 2
![Alt text](imgs/Sender_Option_2.png?raw=true "Optional Title")
* Commandline for sender file execution

![Alt text](imgs/Receiver_Option_2.png?raw=true "Optional Title")
* Commandline for receiver file execution

# Option 3
![Alt text](imgs/Sender_Option_3.png?raw=true "Optional Title")
* Commandline for sender file execution

![Alt text](imgs/Receiver_Option_3.png?raw=true "Optional Title")
* Commandline for receiver file execution

# Option 4
![Alt text](imgs/Sender_Option_4.png?raw=true "Optional Title")
* Commandline for sender file execution

![Alt text](imgs/Receiver_Option_4.png?raw=true "Optional Title")
* Commandline for receiver file execution

# Option 5
![Alt text](imgs/Sender_Option_5.png?raw=true "Optional Title")
* Commandline for sender file execution

![Alt text](imgs/Receiver_Option_5.png?raw=true "Optional Title")
* Commandline for receiver file execution


# Phase 5 Execution Time Graphs

# Plot Illustrating Completion Time For All Five Options  
___
![Alt text](imgs/Graph1_Phase5.jpg?raw=true "Optional Title")
* This graph illustrates the completion time for all 5 options for transferring the same file at 0% loss/error to 70% loss/error in increments of 5%.
* As expected, the execution time with errors related to the ACK packets had essentially no impact on the execution time, as cumulative ACKs are sent back to the sender from the receiver. We do see an increase in execution time after 50% ACK packet related errors, likely because at such high errors, the cumulative ACKs more likely to get lost.
* For error/loss related to data packets, the execution time grew significantly as the percentage raised, up to over 90 seconds at the 70% mark.

# Plot Comparing Execution Time vs. Timeout Value
![Alt text](imgs/Graph2_Phase5.jpg?raw=true "Optional Title")
* This graph shows the execution time for phase 5 as the timeout value was raised from 10 ms to 100 ms in increments of 10 ms. Overall, there is no noticeable impact on the execution time in the presence of ACK packet errors/losses. However, for data packet errors, execution time steadily increased with the timeout value.
* Based on these results, 10 ms appears to be the ideal timeout value.

# Plot Comparing Execution Time vs. Window Size at 20% Error/Loss
![Alt text](imgs/Graph3_Phase5.jpg?raw=true "Optional Title")
* This graph shows the execution time for phase 5 as the window size was adjusted from 1 to 50 packets. 
* We can see that for the ACK related errors, an increase in the window size dramatically lowers execution time, which is expected since we are sending back a cumulative ACK so certain ACK packet drops would not slow down the program significantly.
* On the other hand, error related to data packets steadily raised as the window size increased.
* The best window size would likely be 5 packets to get the benefit of a quick execution time for ACK-related errors while not having the run time for data packet errors being too long.

# Plot Comparing Execution Time by Project Phase for the Bit-Error Options (20%)
![Alt text](imgs/Graph4_Phase5.png?raw=true "Optional Title")
* This graph compares the execution time of transferring an image file between project phases 3, 4 and 5, at 20% error for both the ACK and data packet options
* We see that Phase 5 has the fastest execution time in the event of ACK errors, while Phase 3 had the fastest execution time for data packet losses.
* TCP performance was not as great as Phase 3 or Phase 5, but better than Phase 4.
* Based on this graph, Phase 3 and Phase 5 are the best performers, with Phase 3 likely having a slight edge because of its consistency in execution time for both ACK and Data packet loss/errors.

#Plot Comparing TCP Data Loss and ACK Loss
![Alt text](imgs/Screenshot 2022-12-09 210809.png?raw=true "Optional Title")
* This gragh compares the TCP data loss trendline with the TCP ACK loss trendline
* Data loss yeilds a greater loss rate than ack loss
