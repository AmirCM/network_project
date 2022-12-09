import os
import time


p = 0

while True:
    print(f'Running with p={p}')
    os.system(f'python TCP_Sender.py -p {p}')
    time.sleep(1)
