
import copy
import numpy

from method.adaptor import adapt
from method.cannon_task import parse_to_canon, print_task_as_canon, convert_canon_solution_to_original
from method.input_general import input_general
from method.input_general import input_general_f
from method.simplex import parse_to_standart, init_simplex, simplex
from method.support_vector import support_vector_method

if __name__ == '__main__':
    a = 0


def main():
    signed_indexes, c1, type, A1, b1, A2, b2, A3, b3 = input_general_f("input.txt")
    A, b, c, v, sign_limits, type_opt, value_limits = adapt(signed_indexes, c1, type, A1, b1, A2, b2, A3, b3)

    N, B, A_c, b_c, c_c, v_c, originalSize, originalVars = parse_to_canon(A, b, c, v, sign_limits, type_opt, value_limits)

    print_task_as_canon(A_c, b_c, c_c, v_c)

    A_std, b_std, c_std, v_std, origSize_std, origVar_std = parse_to_standart(A, b, c, v, sign_limits, type_opt, value_limits)

    N_s, B_s, A_s, b_s, c_s, v_s = init_simplex(A_std, b_std, c_std)
    print("simplex solution:")
    solution = convert_canon_solution_to_original(simplex(N_s, B_s, A_s, b_s, c_s, v_s), origSize_std, origVar_std)
    print(solution)
    print(numpy.dot(solution, c))

    print("success")
    target = copy.deepcopy(c_c)
    target.append(type_opt)
    result1 = convert_canon_solution_to_original(support_vector_method(A_c, b_c, target), originalSize, originalVars)
    print(result1)
    print("success")


main()