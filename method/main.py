import copy
import numpy

from method.adaptor import adapt
from method.cannon_task import parse_to_canon, print_task_as_canon, convert_canon_solution_to_original
from method.dual_task import to_dual_task
from method.input_general import input_general
from method.input_general import input_general_f
from method.support_vector import support_vector_method
from method.new_simplex import simplex

if __name__ == '__main__':
    a = 0


def main():
    signed_indexes, c1, type, A1, b1, A2, b2, A3, b3 = input_general_f("input.txt")
    A, b, c, v, sign_limits, type_opt, value_limits = adapt(signed_indexes, c1, type, A1, b1, A2, b2, A3, b3)

    dual_A, dual_b, dual_c, dual_sign_limits, dual_type_opt, dual_value_limits = to_dual_task(A, b, c,
                                                                                              sign_limits,
                                                                                              type_opt,
                                                                                              value_limits)
    dual_v = 0.

    print(type_opt)
    print(c)
    for i in range(len(A)):
        print(A[i], sign_limits[i], b[i])
    print(value_limits)

    print(dual_type_opt)
    print(dual_c)
    for i in range(len(dual_A)):
        print(dual_A[i], dual_sign_limits[i], dual_b[i])
    print(dual_value_limits)

    A_c, b_c, c_c, v_c, originalSize, originalVars = parse_to_canon(A, b, c, v, sign_limits, type_opt,
                                                                          value_limits)


    dual_A_c, dual_b_c, dual_c_c, dual_v_c, dual_originalSize, dual_originalVars = parse_to_canon(
        dual_A, dual_b, dual_c, dual_v, dual_sign_limits, dual_type_opt, dual_value_limits)

    for i in range(len(dual_A_c)):
        print(dual_A_c[i])

    print("canon task:")
    print_task_as_canon(A_c, b_c, c_c, v_c)
    print("dual canon task:")
    print_task_as_canon(dual_A_c, dual_b_c, dual_c_c, dual_v_c)

    print("simplex solution:")
    solution = convert_canon_solution_to_original(simplex(A_c, b_c, c_c, v_c, (type_opt == "max")), originalSize,
                                                  originalVars)
    print(solution)
    print(numpy.dot(solution, c))
    print("success")

    print("vectors solution:")
    target = copy.deepcopy(c_c)
    target.append(type_opt)
    result1 = convert_canon_solution_to_original(support_vector_method(A_c, b_c, target), originalSize, originalVars)
    print(result1)
    print(numpy.dot(result1, c))
    print("success")


    print("simplex solution:")
    solution = convert_canon_solution_to_original(simplex(dual_A_c, dual_b_c, dual_c_c, dual_v_c, (dual_type_opt == "max")), dual_originalSize, dual_originalVars)
    print(solution)
    print(numpy.dot(solution, dual_c))
    print("success")

    M = [0, 1, 2, 3, 4, 5]
    N = [0, 1, 2, 3, 4, 5]
    M1 = [3, 4]
    M2 = [0, 1, 2]
    M3 = [5]
    M13 = [3, 4, 5]
    N1 = [0, 1, 2]
    N2 = [3, 4, 5]

    x = result1
    y = solution
    for i in N1:
        s = 0
        for j in M:
            s += y[j] * A[j][i]
        print(c[i] - s)
    print()
    for i in N2:
        s = 0
        for j in M:
            s += y[j] * A[j][i]
        print(c[i] - s)
    print()

    s0 = 0
    for i in M13:
        s = 0
        for j in N:
            s += x[j] * A[i][j]
        s0 += y[i] * (s - b[i])
    print(s0)

    print()
    s0 = 0
    for i in N1:
        s = 0
        for j in M:
            s += y[j] * A[j][i]
        s0 += x[i] * (c[i] - s)
    print(s0)

    print()
    print("vectors solution:")
    target = copy.deepcopy(dual_c_c)
    target.append(dual_type_opt)
    result1 = convert_canon_solution_to_original(support_vector_method(dual_A_c, dual_b_c, target), dual_originalSize, dual_originalVars)
    print(result1)
    print(numpy.dot(result1, dual_c))
    print("success")


main()
