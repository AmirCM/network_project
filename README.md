# Network Design Project

Authers: Amirhossein Behzadfar, Abhi, Patel, Kalvin McCallum


Phase 3:
Implementation of RDT 2.2 over an unreliable UDP channel with bit-errors. 
---------------------------------------------------------------------
Enviroment 
  -Windows
  -Python 3.9


Submitted Files:
- Sender_Phase3.py - Manages creating and sending packets of the bmp file with header information to the server
- Receiver_Phase3.py - Receive packets, ensures data integrity, and sends acknowledgement back to sender. Reconstructs the image
- select_me.bmp - BMP file used for transfer
- design.md - Design document
- CompletionTime_RawData.xlsx - Excel file containing the raw data for completion time for all three options at different error amounts

Sender/Receiver Instruction
----------------------------------------------------------------------
  * Save the provided BMP file to the appropriate directory. (in imgs sub directory)
  * Ensure that the NumPy module is installed when using PyCharm IDE (done by running "pip install numpy" in command line).
  * For option 1 (no loss/bit-errors), ensure the variable "error_probability" in the sender file and variable "p" in receiver file are set to 0
  * For option 2 (ACK packet bit-error), only the "error_probability" variable in the sender file should equal zero. The other variable should be set to a decimal amount, representing a percentage.
  * For option 3 (data packet bit-error), only the "p" variable in the receiver file should equal zero. The other variable should be set to a decimal amount, representing a percentage.
  * Run the Receiver_Phase3.py first, then run Sender_Phase3.py.
  * Once the BMP file has been transferred between the client and server it will be saved in the project folder.
  * Note: BMP file should be 799 KB and should be named "select_me.bmp" and each packet contains 1024 bytes of data
