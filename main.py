import argparse
import random
import threading
from multiprocessing import Pool

parser = argparse.ArgumentParser()

# Adding arguments for the files to be tested
parser.add_argument('-i', '--input', type=str, help='Input file name', required=True)
parser.add_argument('-o', '--output', type=str, help='Output file name', required=True)
parser.add_argument('-p', '--processes', type=int, help='Number of processes to use', required=False, default=1)

def main():
    matrix = genMatrix(100, 50)
    MAX_PROCESSES = 10
    finalSum = 0

    processPool = Pool(processes=MAX_PROCESSES)
    poolData = list()

    # A process pool allows us to create a pool of worker processes.
    # Each process will accept

    for rowNum in range(len(matrix)):
        matrixData = [matrix, rowNum]
        poolData.append(matrixData)

        finalData = processPool.map(addMatrixRow, poolData)

    del (poolData)

    for num in finalData:
        finalSum += num

    print("The final sum for the matrix is %d." %finalSum)

def addMatrixRow(matrixData):
    matrix = matrixData[0]
    rowNum = matrixData[1]
    del (matrixData)
    rowSum = 0

    for colNum in range(len(matrix[rowNum])):
        rowSum += matrix[rowNum][colNum]
    
    return rowSum

def genMatrix(row, col):
    matrix = list()
    for i in range(row):
        matrix.append(list())
        for j in range(col):
            matrix[i].append(random.randint(0, 10))

    return matrix

if __name__ == "__main__":
    main()