import random, numpy


def gen_matrix_1(n):
    '''all edge inluced with random weight in[0,100]'''
    matrix = [None]*n
    for i in range(n):
            matrix[i] = [round(random.random()*99 + 1, 3) for _ in range(i)]
    return matrix

def gen_matrix_2(n):
    matrix = [None]*n
    for i in range(n):
        matrix[i] = [1 for _ in range(i)]
    return matrix

def write_mat(mat, filename):
    f = open(filename, 'w')
    n = len(mat)
    f.write(str(n)+'\n')
    for i in range(n):
        for j in range(i):
            f.write("{} {} {}\n".format(i, j, mat[i][j]))
    f.close()
    return

def p1_gen():
    size = [25,50,100]
    for i in size:
        mat = gen_matrix_1(i)
        write_mat(mat, 'p1/{}.in'.format(i))

def self_test_gen():
    size = 10
    mat1 = gen_matrix_1(size)
    write_mat(mat1, 'self_test/1.in')
    mat2 = gen_matrix_2(size)
    write_mat(mat2, 'self_test/2.in')


if __name__ == "__main__":
    p1_gen()
    self_test_gen()
