import numpy as np
import argparse

nucleobases = ['C','G','A','T']

parser = argparse.ArgumentParser()
parser.add_argument('max_size', type=int, help='Size of the DNA pattern')
args = parser.parse_args()

for _ in range(args.max_size):
    print((np.random.choice(nucleobases, 1)[0]), end='')
print()

