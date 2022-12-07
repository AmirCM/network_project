import time
from socket import *  # imports socket module to enable network communication
import numpy as np


class TCP:
    def __init__(self):
        self.MSS = 1000
        self.segment = {'source_port': 0,  # 2B
                        'dest_port': 0,  # 2B
                        'seq_num': 0,  # 4B counting bytes of data
                        'ack_num': 0,  # Next expected B
                        'head_len': 0,  # 1B
                        'C': b'0',  # 1 bit congestion
                        'E': b'0',  # 1 bit congestion
                        'U': b'0',  # 1 bit
                        'A': b'0',  # 1 bit Ack
                        'P': b'0',  # 1 bit
                        'R': b'0',  # 1 bit flow
                        'S': b'0',  # 1 bit flow
                        'F': b'0',  # 1 bit flow
                        'rec_window': 0,  # 2B rec window remaining size
                        'checksum': 0,  # 2B
                        }

rtt = 30 / 1000
alpha = 0.25
for _ in range(50):
    stamp = time.time()
    time.sleep(0.6)
    rtt = rtt*(1-alpha) +  (time.time() - stamp)*alpha
    print(rtt, (time.time() - stamp))
