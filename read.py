import string
import numpy
from Utility import *

def read(filename, if_matrix = True):
    '''
    read matrix from <filename>
    if_matrix: True: return adjacent_matrix, False: return Adjacenct_list
    '''
    with open(filename, 'r') as f:
        n = int(f.readline())
        lines_str = f.readlines()
    raw_matrix = [[0 for i in range(n)] for j in range(n)]
    for l in lines_str:
        nums = l.split(' ')
        p = int(nums[0])
        q = int(nums[1])
        m = float(nums[2])
        raw_matrix[p][q] = m
    if if_matrix == True:
        matrix = numpy.array(raw_matrix)
        matrix = matrix + numpy.transpose(matrix)
        return matrix
    else:
        matrix =[]
        for vs in raw_matrix:
            merged_list = tuple(zip(list(range(n)), vs))
            filter_iterator = filter(lambda d: d[1]>0, merged_list)
            matrix.append(list(filter_iterator))
        return matrix

def Print_Matrix(matrix):
    if type(matrix) == 'numpy.ndarray':
        print(matrix)
        return
    for i in matrix:
        print(i)
    return

def read_p1():
    size = [25]
    for s in size:
        mat1 = read("p1/{}.in".format(s), True)
        mat2 = read("p1/{}.in".format(s), False)
        Print_Matrix(mat1)
        print("\n")
        Print_Matrix(mat2)

def read_self_test():
    mat = read("self_test/1.in", True)
    print(isTree(mat))
    Print_Matrix(mat)
    DFS(mat, 0, lambda x:0, lambda x:0)
    Print_Matrix(mat)

if __name__ == "__main__":
    #read_p1()
    read_self_test()
