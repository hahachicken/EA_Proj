import string
import numpy

def read(filename, if_numpy = False):
    with open(filename, 'r') as f:
        n = int(f.readline())
        lines_str = f.readlines()
    matrix = [[-1 for i in range(n)] for j in range(n)]
    for l in lines_str:
        nums = l.split(' ')
        p = int(nums[0])
        q = int(nums[1])
        m = float(nums[2])
        matrix[p][q] = m
    if if_numpy == True:
        matrix = numpy.array(matrix)
    return matrix

def Print_Matrix(matrix):
    if type(matrix) == 'numpy.ndarray':
        print(matrix)
        return
    for i in matrix:
        print(i)
    return

if __name__ == "__main__":
    mat = read("25.in", True)
    Print_Matrix(mat)