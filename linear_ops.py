import math
import random
from itertools import cycle, islice
import numpy as np
from tqdm import tqdm


def shift(row, offset):

    offset = offset % len(row)
    return np.concatenate((row[offset:], row[:offset]))

def sigma_transformation_matrix(m, l):

    transformation_matrix = np.zeros((m*l, m*l))

    for h in range(m*l):
        for i in range(m):
            for j in range(l):

                if h == i + ((i+j) % l) * m:
                    transformation_matrix[i+j*m, h] = 1

    return transformation_matrix


def theta_transformation_matrix(l, n):

    transformation_matrix = np.zeros((l*n, l*n))

    for h in range(l*n):
        for i in range(l):
            for j in range(n):

                if h == ((i+j) % l) + j * l:
                    transformation_matrix[i+j*l, h] = 1

    return transformation_matrix

def epsilon_transformation_matrix(m, n, l, offset = 0):

    transformation_matrix = np.zeros((m*n, m*l))

    for i in range(m*n):
        for j in range(m*l):

            if j == (offset * m + i) % (m*l):
                transformation_matrix[i, j] = 1

    return transformation_matrix


def omega_transformation_matrix(m, n, l, offset = 0):

    transformation_matrix = np.zeros((m*n, n*l))

    for i in range(m*n):
        for j in range(n*l):

            if j == ((offset + (i % m)) % l) + math.floor(i/m) * l:
                transformation_matrix[i, j] = 1

    return transformation_matrix

def hegmm(a, b):

    assert a.ndim == 2, "matmul error: a-matrix number of dimensions must be 2"
    assert b.ndim == 2, "matmul error: b-matrix number of dimensions must be 2"
    assert a.shape[1] == b.shape[0], "matmul error: dimensions incompatable"

    m, l, n = a.shape[0], a.shape[1], b.shape[1]

    A = np.matmul(
        sigma_transformation_matrix(m, l),
        a.copy().flatten(order='F')
    )

    B = np.matmul(
        theta_transformation_matrix(l, n),
        b.copy().flatten(order='F')
    )

    C = np.zeros((a.shape[0] * b.shape[1]))

    for k in range(a.shape[1]):


        lhs = np.matmul(
            epsilon_transformation_matrix(m, n, l, k),
            A.copy()
        )

        rhs = np.matmul(
            omega_transformation_matrix(m, n, l, k),
            B.copy()
        )

        C += np.multiply(lhs, rhs)

    C = C.reshape((m,n), order='F')

    return C


if __name__ == '__main__':

    print("Running test cases...")

    for i in tqdm(range(100)):
        m = random.randint(2,20)
        l = random.randint(2,20)
        n = random.randint(2,20)

        a = np.random.rand(m, l)
        b = np.random.rand(l, n)

        numpy_matmul = np.matmul(a.copy(), b.copy())
        hegmm_matmul = hegmm(a.copy(), b.copy())

        assert(np.allclose(numpy_matmul, hegmm_matmul))

    print("PASSED")
