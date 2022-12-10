# Phase 6 design doc by Amirhossein Behzadfar, Abhi Patel, and Kalvin McCallum
___
# Introduction
___
Phase 6 of the network design project involves the implementation of TCP. The aspects implemented are RDT, connection setup, connection teardown, dynamic window size, dynamic timeout, checksum, flow control, congestion control (Tahoe).

# Phase 6 Execution Time Graphs

# Plot Comparing Execution Time by Project Phase for the Bit-Error Options (20%)
![Alt text](imgs/Graph4_Phase5.png?raw=true "Optional Title")
* This graph compares the execution time of transferring an image file between project phases 3, 4 and 5, at 20% error for both the ACK and data packet options
* We see that Phase 5 has the fastest execution time in the event of ACK errors, while Phase 3 had the fastest execution time for data packet losses.
* TCP performance was not as great as Phase 3 or Phase 5, but better than Phase 4.
* Based on this graph, Phase 3 and Phase 5 are the best performers, with Phase 3 likely having a slight edge because of its consistency in execution time for both ACK and Data packet loss/errors.

# Plot Comparing TCP Data Loss and ACK Loss
![Alt text](imgs/TCP_Chart.png?raw=true "Optional Title")
* This gragh compares the TCP data loss trendline with the TCP ACK loss trendline
* Data loss hurts the execution time of the program more than ACK loss.
