import argparse
import multiprocessing

n = None

# Function to parse command line arguments
def parse_args():
    parser = argparse.ArgumentParser(description="Execute cellular life simulator over 100 time steps.")
    parser.add_argument('-i', '--input', type=str, help='Input file name', required=True)
    parser.add_argument('-o', '--output', type=str, help='Output file name', required=True)
    parser.add_argument('-p', '--processes', type=int, help='Number of processes to use', required=False, default=1)
    return parser.parse_args()

# Function to read matrix from file
def read_matrix(file_name, matrix):
    with open(file_name, 'r') as file:
        for line in file:
            row = list(line.strip())
            matrix.append(row)
    return matrix

# Function to write matrix to file
def write_matrix(file_name, matrix):
    with open(file_name, 'w') as file:
        for row in matrix:
            file.write(''.join(row) + '\n')

# Function to get all neighbor positions using precomputed x and y adjustments
def get_neighbors(x, y):
    xm1, xp1 = (x-1) % n, (x+1) % n
    ym1, yp1 = (y-1) % n, (y+1) % n
    return [(xm1, ym1), (xm1, y), (xm1, yp1),
            (x, ym1), (x, yp1),
            (xp1, ym1), (xp1, y), (xp1, yp1)]

# Function to get neighbor count
def get_neighbor_count(matrix, x, y):
    neighbors = get_neighbors(x, y)
    return sum(1 for i, j in neighbors if matrix[i][j] == 'O')

# Function to check if number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num**0.5) + 1):
        if num % i == 0:
            return False
    return True

# Function to update cell
def update_cell(matrix, x, y):
    alive = matrix[x][y] == 'O'
    neighbors = get_neighbor_count(matrix, x, y)
    valid_neighbors = {2, 4, 6, 8}
    if alive:
        return 'O' if is_prime(neighbors) else '.'
    else:
        return 'O' if neighbors in valid_neighbors else '.'

# Function to process generation for rules
def process_generation(current_matrix):
    n = len(current_matrix)
    new_matrix = [[None]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            new_matrix[i][j] = update_cell(current_matrix, i, j)
    return new_matrix

# Function to simulate 100 steps
def simulate(matrix):
    for _ in range(100):
        matrix = process_generation(matrix)
    return matrix

# Main function
def main():
    print("Project:: Cellular Life Simulator R#11736897\n")
    args = parse_args()
    global n
    input_matrix = read_matrix(args.input)
    n = len(input_matrix)
    final_matrix = simulate(input_matrix, 100)
    write_matrix(args.output, final_matrix)

if __name__ == "__main__":
    main()
