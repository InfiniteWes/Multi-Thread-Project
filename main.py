"""
=====================================================================
Title:              Wesley_Spangler_R11736897.py
Description:        Python 3 Project for Multiprocessing
Author:             Wesley Spangler
Date:               4/20/24
Version:            1.0
Usage:              python3 Wesley_Spangler_R11736897.py
Notes:              This project has no requirements besides python
Python Version:     3.12.3
=====================================================================
"""

import argparse
import multiprocessing as mp

valid_neighbors = {2, 4, 6, 8}
neighbor_coords = {}
prime = {2,3,5,7}
offsets = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
shared_matrix = None

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Execute cellular life simulator over 100 time steps.")
    parser.add_argument('-i', '--input',type=str, help='Input file name', required=True)
    parser.add_argument('-o', '--output',type=str, help='Output file name', required=True)
    parser.add_argument('-p', '--processes',type=int, help='Number of processes to use', required=False, default=1)
    return parser.parse_args()

# Read matrix from file
def read_matrix(file_name):
    matrix = []
    with open(file_name, 'r') as file:
        for line in file:
            row = list(line.strip())
            matrix.append(row)
    return matrix

# Write matrix to file
def write_matrix(file_name, matrix):
    with open(file_name, 'w') as file:
        for row in matrix:
            file.write(''.join(row) + '\n')

# get all neighbor positions
def get_neighbors(n):
     # Compute neighbors for each cell using precomputed offsets
    for x in range(n):
        for y in range(n):
            neighbor_coords[(x, y)] = [((x + dx) % n, (y + dy) % n) for dx, dy in offsets]

# Initialize multiprocessing context with shared matrix
def init_process(shared_mat):
    global shared_matrix
    shared_matrix = shared_mat

# Get neighbor count
def get_neighbor_count(matrix, x, y, n):
    return sum(1 for i, j in neighbor_coords[(x, y)] if matrix[i][j] == 'O')

def update_cell(matrix, x, y, n):    
    # Determine if the matrix cell is alive
    alive = matrix[x][y] == 'O'
    # Count how many neighbors are alive
    neighbors = get_neighbor_count(matrix, x, y, n)

    # Check if the number of neighbors is in the set of primes
    is_prime = neighbors in prime

    # Update cell based on life status and prime condition
    if alive:
        return 'O' if is_prime else '.'
    else:
        return 'O' if neighbors in valid_neighbors else '.'


# Process rows in parallel
def process_rows(args):
    row_index, n = args
    matrix = shared_memory(n)
    new_row = [update_cell(matrix, row_index, j, n) for j in range(len(matrix[0]))]
    return new_row

# Convert matrix to shared memory array
def matrix_to_shared(matrix, n):
    return mp.Array('c', ''.join([''.join(row) for row in matrix]).encode(), lock=False)

# Access shared memory matrix
def shared_memory(n):
    global shared_matrix
    return [shared_matrix[i*n:(i+1)*n].decode() for i in range(n)]

# Process generation
def process_generation(num_processes, n):
    with mp.Pool(processes=num_processes, initializer=init_process, initargs=(shared_matrix,)) as pool:
        args_list = [(i, n) for i in range(n)]
        result = pool.map(process_rows, args_list)
        for i, new_row in enumerate(result):
            shared_matrix[i*n:(i+1)*n] = ''.join(new_row).encode()

# Simulate 100 steps
def simulate(matrix, num_processes):
    n = len(matrix)
    global shared_matrix
    shared_matrix = matrix_to_shared(matrix, n)
    get_neighbors(n)
    for _ in range(100):
        process_generation(num_processes, n)
    return shared_memory(n)

def main():
    args = parse_args()
    input_matrix = read_matrix(args.input)
    final_matrix = simulate(input_matrix, args.processes)
    write_matrix(args.output, final_matrix)

if __name__ == "__main__":
    main()
