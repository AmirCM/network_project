import os
import time
p = 0
i = 0
while True:
    print(f'{i} Running with p={p}')
    os.system(f'python TCP_Receiver.py -p {p}')
    time.sleep(0.5)
    # p += 0.05
    i += 1
    if p > 12:
        break
