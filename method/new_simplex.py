import copy
import math

eps = 1e-10


def build_bad(source_A: list[list[float]], source_b: list[float], source_c: list[float], source_v: float):
    m = len(source_A)
    n = len(source_A[0])
    t_A = copy.deepcopy(source_A)
    t_b = copy.deepcopy(source_b)
    t_c = copy.deepcopy(source_c)
    t_v = source_v
    basis_list = [-1 for i in range(m)]
    for i in range(m):
        e = -1
        for j in range(n):
            if abs(t_A[i][j]) > eps:
                e = j
                break
        if e == -1:
            raise Exception("Err 2")
        basis_list[i] = e
        a_ie = t_A[i][e]
        t_b[i] /= a_ie
        for j in range(n):
            t_A[i][j] /= a_ie

        for k in range(m):
            if k == i:
                continue
            t_b[k] -= t_b[i] * t_A[k][e]
            for j in range(n):
                if j == e:
                    continue
                t_A[k][j] -= t_A[i][j] * t_A[k][e]

        for j in range(n):
            if j == e:
                continue
            t_c[j] -= t_c[e] * t_A[i][j]
        t_v += t_c[e] * t_b[i]
        t_c[e] = 0.
        for k in range(m):
            t_A[k][e] = 0.

    return t_A, t_b, t_c, t_v, basis_list


def pivot(A: list[list[float]], b: list[float], c: list[float], v: float, basis: list[int], nulls: list[int], l: int,
          e: int):
    n_A = [[0. for i in range(len(A[0]))] for j in range(len(A))]
    n_b = [0. for i in range(len(b))]
    n_c = [0. for i in range(len(c))]

    n_b[e] = b[l] / A[l][e]

    for j in nulls:
        if j == e:
            continue
        n_A[e][j] = A[l][j] / A[l][e]
    n_A[e][l] = 1 / A[l][e]

    for i in basis:
        if i == l:
            continue
        n_b[i] = b[i] - A[i][e] * n_b[e]
        for j in nulls:
            if j == e:
                continue
            n_A[i][j] = A[i][j] - A[i][e] * n_A[e][j]
        n_A[i][l] = -A[i][e] * n_A[e][l]

    n_v = v + c[e] * n_b[e]

    for j in nulls:
        if j == e:
            continue
        n_c[j] = c[j] - c[e] * n_A[e][j]
    n_c[l] = -c[e] * n_A[e][l]

    for j in range(len(nulls)):
        if nulls[j] == e:
            nulls[j] = l
            break
    for i in range(len(basis)):
        if basis[i] == l:
            basis[i] = e
            break

    return n_A, n_b, n_c, n_v, basis, nulls


def simplex_init(source_A: list[list[float]], source_b: list[float], source_c: list[float], source_v: float):
    m = len(source_A)
    n = len(source_A[0])
    t_A, t_b, t_c, t_v, basis_list = build_bad(source_A, source_b, source_c, source_v)

    A = [list() for i in range(n)]
    b = [0. for i in range(n)]
    c = copy.deepcopy(t_c)
    v = t_v
    for i in range(n):
        if i in basis_list:
            j = basis_list.index(i)
            A[i] = t_A[j]
            b[i] = t_b[j]
        else:
            A[i] = [0. for j in range(n)]
            b[i] = 0.
    basis = copy.deepcopy(basis_list)
    nulls = list()
    for i in range(n):
        if i not in basis:
            nulls.append(i)

    k = 0
    for i in range(n):
        if b[i] < b[k]:
            k = i

    if b[k] >= 0:
        return A, b, c, v, basis, nulls

    s_A = A
    s_b = copy.deepcopy(b)
    s_b.append(0.)
    s_c = [-1. if i == n else 0 for i in range(n + 1)]
    s_v = 0.
    s_is_max = True
    s_basis = copy.deepcopy(basis)
    s_nulls = copy.deepcopy(nulls)
    for i in s_basis:
        s_A[i].append(-1.)
    for i in s_nulls:
        s_A[i].append(0.)
    s_nulls.append(n)
    s_A.append([0. for i in range(n + 1)])
    s_A, s_b, s_c, s_v, s_basis, s_nulls = pivot(s_A, s_b, s_c, s_v, s_basis, s_nulls, k, n)
    s_x, s_A, s_b, s_c, s_v, s_basis, s_nulls = simplex_iterate(s_A, s_b, s_c, s_v,
                                                                s_basis, s_nulls,
                                                                s_is_max)
    if abs(s_x[n]) > eps:
        return -1
    if n in s_basis:
        e = -1
        for i in s_nulls:
            if s_A[i][n] != 0:
                e = i
                break
        if e == -1:
            raise Exception("Err 3")
        s_A, s_b, s_c, s_v, s_basis, s_nulls = pivot(s_A, s_b, s_c, s_v, s_basis, s_nulls, n, e)
    s_A.pop()
    s_b.pop()
    s_nulls.remove(n)
    for i in range(n):
        s_A[i].pop()

    A = s_A
    b = s_b
    basis = s_basis
    nulls = s_nulls
    for i in basis:
        for j in nulls:
            c[j] -= c[i] * A[i][j]
        v += c[i] * b[i]
        c[i] = 0.

    return A, b, c, v, basis, nulls


def simplex(source_A: list[list[float]], source_b: list[float], source_c: list[float], source_v: float, is_max: bool):
    A, b, c, v, basis, nulls = simplex_init(source_A, source_b, source_c, source_v)

    x, A, b, c, v, basis, nulls = simplex_iterate(A, b, c, v, basis, nulls, is_max)

    return x


def simplex_iterate(A: list[list[float]], b: list[float], c: list[float], v: float, basis: list[int], nulls: list[int],
                    is_max: bool):
    less = lambda a1, a2: a1 < a2
    more = lambda a1, a2: a1 > a2
    comparator = more if is_max else less
    delta_list = [0. for i in range(len(b))]
    while True:
        e = -1
        for j in nulls:
            if comparator(c[j], 0):
                e = j
                break
        if e == -1:
            break
        for i in basis:
            if A[i][e] > 0:
                delta_list[i] = b[i] / A[i][e]
            else:
                delta_list[i] = math.inf
        l = -1
        for i in basis:
            if l == -1 or delta_list[i] < delta_list[l]:
                l = i
        if delta_list[l] == math.inf:
            return [-1.], A, b, c, v, basis, nulls
        A, b, c, v, basis, nulls = pivot(A, b, c, v, basis, nulls, l, e)
    x = [(b[i] if i in basis else 0.) for i in range(len(A))]
    return x, A, b, c, v, basis, nulls
