import copy
import sys


def initialize_simplex(A, b, c):
    rows = len(A)
    cols = len(A[0])

    N = [i for i in range(cols)]
    B = [cols + i for i in range(rows)]
    c = [c[idx] if idx < len(c) else 0 for idx in range(rows + cols)]
    b_new = [0 if idx < cols else b[idx - cols] for idx in range(rows + cols)]
    A_new = [[0 for j in range(rows + cols)] for i in range(rows + cols)]

    for i in range(rows):
        for j in range(cols):
            A_new[i + cols][j] = A[i][j]

    return N, B, A_new, b_new, c, 0


def pivot(N: list, B: list, A: list, b: list, c: list, v: int, l: int, e: int):
    b_new = [0 for i in range(len(b))]
    b_new = b[l] / A[l][e]

    N_new = copy.deepcopy(N)
    B_new = copy.deepcopy(B)
    A_new = [[0 for i in range(len(A[0]))] for j in range(len(A))]
    for j in N:
        if j != e:
            A_new[e][j] = A[l][j] / A[l][e]
    A_new[e][l] = 1 / A[l][e]

    for i in B:
        if i != l:
            b_new[i] = b[i] - A[i][e] * b_new[e]
            for j in N:
                if j != e:
                    A_new[i][j] = A[i][j] - A[i][e] * A_new[e][j]
            A_new[i][l] = -A[i][e] * A_new[e][l]

    v_new = v + c[e] * b_new[e]
    c_new = [0 for i in range(len(b))]
    for j in N:
        if j != e:
            c_new[j] = c[j] - c[e] * A_new[e][j]
    c_new[l] = -c[e] * A_new[e][l]

    if e in N:
        N_new.remove(e)
    N_new.append(l)

    if l in B:
        B_new.remove(l)
    B_new.append(e)

    return N_new, B_new, A_new, b_new, c_new, v_new


def minimize_index(delta: list, B: list):
    ''' мое решение
    min = sys.maxsize
    min_idx = -1
    for idx, val in enumerate(delta):
        if idx not in B or val == "inf":
            continue

        if val < min:
            min = val
            min_idx = idx
    return min_idx
    '''

    # скопипастил
    for idx, val in enumerate(delta):
        if idx not in B:
            continue

        min = val
        min_idx = idx

        if min != "inf":
            break

    if min == "inf":
        return min_idx

    for idx, val in enumerate(delta):
        if idx not in B:
            continue

        if val == "inf":
            continue

        if val < min:
            min = val
            min_idx = idx

    return min_idx


def simplex_method(A: list, b: list, c: list):
    N, B, A, b, c, v = initialize_simplex(A, b, c)

    delta = [0 for i in range(len(A))]
    x = list()
    while (True):
        e = -1
        for j in N:
            if c[j] > 0:
                e = j
                break  # delete ?

        if e == -1:
            break

        for i in B:
            if A[i][e] > 0:
                delta[i] = b[i] / A[i][e]
            else:
                delta[i] = "inf"

        l = minimize_index(delta, B)
        if delta[l] == "inf":
            raise Exception("Задача неограничена")
        else:
            N, B, A, b, c, v = pivot(N,B,A,b,c,v,l,e)

        for i in range(1, len(A)):
            if i in B:
                x.append(b[i])
            else:
                x.append(0)

    return x
