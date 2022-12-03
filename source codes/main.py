import os
import argparse
from multiprocessing import Pool

processes = ('Receiver_Phase4.py', 'sender_ph5.py')


def run_process(process):
    os.system('python {}'.format(process))




arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-o', type=int, required=True)
arg_parser.add_argument('-p', type=float, required=False)
arg_parser.add_argument('-N', type=int, required=True)
args = arg_parser.parse_args()
p = 0
if args.o <= 5:
    if args.p:
        p = args.p
    pool = Pool(processes=2)
    pool.map(run_process, 'Receiver_Phase4.py')
    pool.map(run_process, 'sender_ph5.py')

    os.system(f"start /wait cmd /k python Receiver_Phase4.py -o {args.o} -p {p}")
    os.system(f'start /wait cmd /k python sender_ph5.py -o {args.o} -p {p} -N {args.N}')

else:
    print(f'Invalid input! {args.o} only option 1 ~ 5')

