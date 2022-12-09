import os
import time
p = 0
while True:
    print(f'Running with p={p}')
    os.system(f'python TCP_Receiver.py -p {p}')
    time.sleep(0.5)
    p += 0.05
    if p > 0.6:
        break
