import os
import time
p = 0.6
i = 0
while True:
    print(f'{i} Running with p={p}')
    os.system(f'python TCP_Receiver.py -p {p}')
    time.sleep(0.85)
    p += 0.05
    i += 1
    if p > 0.8:
        break
