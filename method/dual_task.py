import string


def copyMatr(A: list):
    A_copy = list()
    for i in range(len(A)):
        A_copy.append([A[i][j] for j in range(len(A[i]))])
    return A_copy


def copyVec(A: list):
    A_copy = list()
    for i in range(len(A)):
        A_copy.append(float(A[i]))
    return A_copy


def takeColumn(matrix: list, indx: int):
    return [matrix_line[indx] for matrix_line in matrix]


def to_dual_task(A: list, b: list, c: list, sign_limits: list, value_limits: list, type_opt: string):
    A_dual = list()
    limSigns_dual = list()
    valuesLimits_dual = list()

    limitsCnt = len(sign_limits)
    valuesCnt = len(c)

    A_tmp = copyMatr(A)

    # change all limits expressions
    for i in range(limitsCnt):
        if (sign_limits[i] == ">=" and type_opt == "max") or (sign_limits[i] == "<=" and type_opt == "min"):
            if sign_limits[i] == ">=":
                sign_limits[i] = "<="
            else:
                sign_limits[i] = ">="

            for j in range(len(A_tmp[i])):
                A_tmp[i][j] = -1 * A_tmp[i][j]
            b[i] = b[i] * -1

    # set dual target extremum
    if type_opt == "min":
        type_opt_dual = "max"
        expr_d_sign = "<="
    else:
        type_opt_dual = "min"
        expr_d_sign = ">="

    # swap b and c
    c_d = b
    b_d = c

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
        if sign_limits[i] != "=":
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
