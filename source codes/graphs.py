import os
import time
import matplotlib.pyplot as plt

p = 0
while True:
    print(f'Running with p={p}')
    T = time.time()
    os.system(f'python TCP_Sender.py -p {p}')
    print(f'time: {time.time()-T}')
    input('Next?')
