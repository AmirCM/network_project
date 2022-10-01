# Network Design Project

Authers: Amirhossein Behzadfar, Abhi, Patel, Kalvin McCallum

Phase 1:
UDP server/ client
---------------------------------------------------------------------
Enviroment 
  -Windows
  -Python 3.9


Server/Client Instruction
----------------------------------------------------------------------
  * First run the server.py, then run client.py by passing your desired message as a argument. e.g. python client.py "Hello !!!"
  * If you pass "exit" by using client, the server will be terminated. 
  * Note: Msg should be less than 2048 Bytes 

Phase 2:
Implementation of RDT 1.0 over a reliable UDP channel. 
---------------------------------------------------------------------
Enviroment 
  -Windows
  -Python 3.9


Submitted Files:
- Sender_Phase2.py - Parse BMP file into packets and send to the receiver
- Receiver_Phase2.py - Receive packets and reconstruct the BMP file
- GUI_client.py - GUI for the sender side
- GUI_server.py - GUI for the receiver side
- select_me.bmp - BMP file used for transfer
- design.md - Design document



Sender/Receiver Instruction
----------------------------------------------------------------------
  * Save the provided BMP file to the appropriate directory.
  * Run the Receiver_Phase2.py first, then run Sender_Phase2.py by passing the BMP file as packets. 
  * Once the the BMP file has been transferred between the client and server it will be saved in the project folder.
  * Open the recevied image to ensure that no bits were lost during transfer.
  * Note: BMP file should be 799 KB and should be named "select me.bmp" and each packet created is of size 1024 Bytes

GUI Instruction
----------------------------------------------------------------------
  * Before running the GUI ensure that the pip pillow module is installed when using PyCharm IDE.
  * This can be done by using the "pip install pillow" command line.
  * Begin by running GUI_server.py and wait for the GUI server window to open.
  * Once the GUI server window opens, run GUI_client.py and wait for the GUI client window to open.
  * On the GUI server window click on the "Start Server" button in the bottom left-hand corner.
  * Then click on the "Select Image" button in the bottom left-hand corner of the GUI client window and select the BMP file "select me.bmp".
  * Click on the "Send Image" button in the bottom left-hand corner of the GUI client window and wait for message to appear on GUI server window.
  * Once the GUI server window displays "Incoming image received!!!", click on the "Show Image" button in the bottom left corner of the GUI server window.
