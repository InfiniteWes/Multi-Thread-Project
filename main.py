import argparse
import random
import threading
from multiprocessing import Pool

parser = argparse.ArgumentParser()

# Adding arguments for the files to be tested
def parse_args():
    parser.add_argument('-i', '--input', type=str, help='Input file name', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output file name', required=True)
    parser.add_argument('-p', '--processes', type=int, help='Number of processes to use', required=False, default=1)
    return parser.parse_args()

def read_matrix(file_name):
    matrix = []
    with open(file_name, 'r') as file:
        for line in file:
            matrix.append([str(x) for x in line.split()])
    return matrix

def write_matrix(file_name, matrix):
    with open(file_name, 'w') as file:
        for row in matrix:
            file.write(' '.join([str(x) for x in row]) + '\n')

if __name__ == "__main__":
    args = parse_args()
    matrix = read_matrix(args.input)