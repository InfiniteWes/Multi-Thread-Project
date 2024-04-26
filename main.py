import argparse
import multiprocessing as mp

# Parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Execute cellular life simulator over 100 time steps.")
    parser.add_argument('-i', '--input', type=str, help='Input file name', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output file name', required=True)
    parser.add_argument('-p', '--processes', type=int, help='Number of processes to use', required=False, default=1)
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

# Get all neighbor positions using precomputed x and y adjustments
def get_neighbors(x, y, n):
    xm1, xp1 = (x-1) % n, (x+1) % n
    ym1, yp1 = (y-1) % n, (y+1) % n
    return [(xm1, ym1), (xm1, y), (xm1, yp1),
            (x, ym1), (x, yp1),
            (xp1, ym1), (xp1, y), (xp1, yp1)]

# Get neighbor count
def get_neighbor_count(matrix, x, y, n):
    neighbors = get_neighbors(x, y, n)
    return sum(1 for i, j in neighbors if matrix[i][j] == 'O')

# Check if number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Update cell
def update_cell(matrix, x, y, n):
    alive = matrix[x][y] == 'O'
    neighbors = get_neighbor_count(matrix, x, y, n)
    valid_neighbors = {2, 4, 6, 8}
    if alive:
        return 'O' if is_prime(neighbors) else '.'
    else:
        return 'O' if neighbors in valid_neighbors else '.'

# Process rows in parallel
def process_rows(args):
    matrix, row_index, n = args
    new_row = [update_cell(matrix, row_index, j, n) for j in range(len(matrix[0]))]
    return new_row

# Process generation
def process_generation(matrix, num_processes):
    n = len(matrix)
    if n == 0:
        raise ValueError("Input matrix is empty and cannot be processed.")
    with mp.Pool(num_processes) as pool:
        args_list = [(matrix, i, n) for i in range(n)]
        new_matrix = pool.map(process_rows, args_list)
    return new_matrix


# Simulate 100 steps
def simulate(matrix, num_processes):
    for _ in range(100):
        matrix = process_generation(matrix, num_processes)
    return matrix

def main():
    args = parse_args()
    input_matrix = read_matrix(args.input)
    n = len(input_matrix)

    # Simulate and write the final matrix using multiprocessing
    final_matrix = simulate(input_matrix, args.processes)
    write_matrix(args.output, final_matrix)

if __name__ == "__main__":
    main()
