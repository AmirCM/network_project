# Phase 1 design doc by Amirhossein Behzadfar
___
Establishing a UDP connection between two processes in a same host. Sending a msg from client and receiving an echo response from the server.

# Server code
___
![Alt text](./server_snap.png?raw=true "Optional Title")
* Initiate a UDP socket (SOCK_DGRAM), then in a while loop listen to the given port and any host.
* After getting the incoming data, we will send it back to client. 
* In case of getting 'exit' command the loop will break

# Client code
___
![Alt text](./client_snap.png?raw=true "Optional Title")
* Initiate a UDP socket (SOCK_DGRAM), with the given port that server is listening to and the local host.
* Sending the argument value passed to the code. 
* Receiving the response from the server

# Execution
___
![Alt text](./phase_1.png?raw=true "Optional Title")