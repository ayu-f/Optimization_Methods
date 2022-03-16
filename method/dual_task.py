import copy
import string






def takeColumn(matrix: list, indx: int):
    return [matrix_line[indx] for matrix_line in matrix]


def to_dual_task(A: list, b: list, c: list, sign_limits: list, type_opt: string, value_limits: list):
    A_dual = list()
    limSigns_dual = list()
    valuesLimits_dual = list()

    limitsCnt = len(sign_limits)
    valuesCnt = len(c)

    b_tmp = copy.deepcopy(b)
    A_tmp = copy.deepcopy(A)
    sign_limits_tmp = copy.deepcopy(sign_limits)

    # change all limits expressions
    for i in range(limitsCnt):
        if (sign_limits_tmp[i] == ">=" and type_opt == "max") or (sign_limits_tmp[i] == "<=" and type_opt == "min"):
            if sign_limits_tmp[i] == ">=":
                sign_limits_tmp[i] = "<="
            else:
                sign_limits_tmp[i] = ">="

            for j in range(len(A_tmp[i])):
                A_tmp[i][j] = -A_tmp[i][j]
            b_tmp[i] = -b_tmp[i]

    # set dual target extremum
    if type_opt == "min":
        type_opt_dual = "max"
        expr_d_sign = "<="
    else:
        type_opt_dual = "min"
        expr_d_sign = ">="

    # swap b and c
    c_d = b_tmp
    b_d = copy.deepcopy(c)

    # trasponate
    for i in range(len(A_tmp[0])):
        A_dual.append(takeColumn(A_tmp, i))

    # set limits signs
    for i in range(len(c)):
        if i in value_limits:
            limSigns_dual.append(expr_d_sign)
        else:
            limSigns_dual.append("=")

    # set values signs
    for i in range(limitsCnt):
        if sign_limits_tmp[i] != "=":
            valuesLimits_dual.append(i)

    return A_dual, b_d, c_d, limSigns_dual, type_opt_dual, valuesLimits_dual


def print_task_as_dual(A_d: list, b_d: list, c_d: list, v_d: float, limSigns_d: list, extrSign_d: str,
                       valuesLimits_d: list):
    str_to_out = extrSign_d + ": target = " + str(v_d)
    for i in range(len(c_d)):
        str_to_out += " + " + str(c_d[i]) + " * y" + str(i + 1)
    print(str_to_out)

    for i in range(len(A_d)):
        str_to_out = ""
        for j in range(len(A_d[i])):
            str_to_out += str(A_d[i][j]) + " * y" + str(j + 1)
            if j != len(A_d[i]) - 1:
                str_to_out += " + "
        str_to_out += " " + limSigns_d[i] + " " + str(b_d[i])
        print(str_to_out)

    for i in range(len(c_d)):
        if i in valuesLimits_d:
            str_to_out = "y" + str(i + 1) + " >= 0"
            print(str_to_out)

    return
