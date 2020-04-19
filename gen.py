import random, numpy
import utility, read

def R():
    return round(random.random()*99 + 1, 3)

def gen_matrix_1(n):
    '''all edge inluced with random weight in[0,100]'''
    matrix = [None]*n
    for i in range(n):
            matrix[i] = [R() for _ in range(i)]
    return matrix

def gen_matrix_2(n):
    matrix = [None]*n
    for i in range(n):
        matrix[i] = [1 for _ in range(i)]
    return matrix

def gen_matrix_3(n):
    matrix = [[0 for _1 in range(n)] for _2 in range(n)]
    for i in range(1, n):
        matrix[i][i-1] = R()
    for i in range(n):
        for j in range(n):
            if i == j: 
                continue
            t = random.randint(0, n)
            if t < 4 and matrix[i][j] == 0:
                matrix[i][j] = R()
    return matrix

def write_mat(matrix, filename):
    np_matrix = numpy.array(matrix)
    np_matrix = np_matrix + numpy.transpose(np_matrix)
    f = open(filename, 'w')
    n = len(matrix)
    f.write(str(n)+'\n')
    for i in range(n):
        for j in range(i):
            if matrix[i][j] != 0: 
                f.write("{} {} {}\n".format(i, j, matrix[i][j]))
    f.close()
    return

def p1_gen():
    size = [25,50,100]
    for i in size:
        mat = gen_matrix_3(i)
        write_mat(mat, 'p1/{}.in'.format(i))

def self_test_gen():
    size = 15
    for i in range(10):
        mat = gen_matrix_3(size)
        write_mat(mat, 'self_test/{}.in'.format(i))

if __name__ == "__main__":
    #p1_gen()
    #read.read_p1()
    self_test_gen()
