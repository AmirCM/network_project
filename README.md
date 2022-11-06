# Network Design Project

Authers: Amirhossein Behzadfar, Abhi, Patel, Kalvin McCallum


Phase 4:
Implementation of RDT 3.0 over an unreliable UDP channel with bit-errors and losses. 
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
  * Save all necessary provided files (two python files and BMP file) in the same directory
  * Ensure that the NumPy module is installed when using PyCharm IDE (done by running "pip install numpy" in command line).
  * Open two command windows
  * Navigate to the directory where the python scripts and bmp file are stored.
  * Run the Receiver_Phase3.py first in one window, then run Sender_Phase3.py in the other window.
  * Option 1: The command is as follows the -p can be changed (0~1)
    * python Receiver_Phase3.py -o 1 -p 0.0
    * python Sender_Phase3.py -o 1 -p 0.0
  * Option 2: The command is as follows the -p can be changed (0~1)
    * python Receiver_Phase3.py -o 2 -p 0.01
    * python Sender_Phase3.py -o 2 
  * Option 3: The command is as follows the -p can be changed (0~1)
    * python Receiver_Phase3.py -o 3
    * python Sender_Phase3.py -o 3 -p 0.01
  * Option 4: The command is as follows the -p can be changed (0~1)
    * python Receiver_Phase3.py -o 4
    * python Sender_Phase3.py -o 4 -p 0.01
  * Option 5: The command is as follows the -p can be changed (0~1)
    * python Receiver_Phase3.py -o 5 -p 0.01
    * python Sender_Phase3.py -o 5
  * Once the BMP file has been transferred between the client and server it will be saved in the directory folder.
  * Note: BMP file should be 799 KB and should be named "select_me.bmp" and each packet contains 1024 bytes of data
