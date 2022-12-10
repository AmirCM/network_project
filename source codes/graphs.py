import os
import time


p = 0.6
while True:
    print(f'Running with p={p}')
    os.system(f'python TCP_Sender.py -p {0}')

    time.sleep(2.5)
    p += 0.05
    if p > 0.8:
        break
