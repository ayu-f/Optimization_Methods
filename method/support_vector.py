from itertools import combinations
import numpy


def generate_all_matrix(matrix: numpy.ndarray): # generate all matrix with det != 0
    all_bases_matrix = []
    combination = []
    indexes = [i for i in range(matrix.shape[1])]

    for i in combinations(indexes, matrix.shape[0]):
        bases_matrix = matrix[:, i]
        if numpy.linalg.det(bases_matrix) != 0:
            all_bases_matrix.append(bases_matrix)
            combination.append(i)

    return all_bases_matrix, combination


def get_support_vectors(matrix: list, free_members: list): # find all vectors (solution Ax=B for all generated matrix)
    vectors = []
    if len(matrix) >= len(matrix[0]):
        return []
    bases_matrix, indexes = generate_all_matrix(numpy.array(matrix))

    for i in range(len(bases_matrix)):
        result = numpy.linalg.solve(bases_matrix[i], free_members)
        if len(result[result < 0]) != 0:
            continue
        if len(result[result > 1e+16]) != 0:
            continue

        base = []
        for j in range(len(matrix[0])):
            base.append(0)
        for j in range(len(indexes[i])):
            base[indexes[i][j]] = result[j]
        vectors.append(base)

    return vectors


def support_vector_method(matrix: list, free_members: list, target: list):
    if target[len(target) - 1] == "max":
        for i in range(len(target) - 1):
            target[i] = -target[i]
    target.pop()

    bases = get_support_vectors(matrix, free_members)
    if len(bases) == 0:
        return []

    result = bases[0]
    for i in range(len(bases)):
        if numpy.dot(bases[i], target) < numpy.dot(result, target):
            result = bases[i]

    return result

