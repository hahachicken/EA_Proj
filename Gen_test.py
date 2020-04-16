import random, numpy


def Gen_Matrix1(n):
    '''all edge inluced with random weight in[0,100]'''
    matrix = [None]*n
    for i in range(n):
            matrix[i] = [round(random.random()*100, 3) for _ in range(n)]
    return matrix

def WriteMat(mat, filename):
    f = open(filename, 'w')
    n = len(mat)
    f.write(str(n)+'\n')
    for i in range(n):
        for j in range(n):
            f.write("{} {} {}\n".format(i, j, mat[i][j]))
    f.close()
    return

if __name__ == "__main__":
    size = [5,25,50,100]
    for i in size:
        mat = Gen_Matrix1(i)
        WriteMat(mat, '{}.in'.format(i))