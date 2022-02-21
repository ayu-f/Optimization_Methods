import copy


def adapt(signed_indexes: list[int], c1: list[float], type: str, A1: list[list[float]], b1: list[float], A2: list[list[float]], b2: list[float], A3: list[list[float]], b3: list[float]):
    A = list()
    b = list()
    c = copy.deepcopy(c1)
    v = 0
    sign_limits = list()
    type_opt = type
    value_limits = copy.deepcopy(signed_indexes)
    for i in range(len(A1)):
        A.append(A1[i])
        b.append(b1[i])
        sign_limits.append("=")
    for i in range(len(A3)):
        A.append(A3[i])
        b.append(b3[i])
        sign_limits.append(">=")
    for i in range(len(A2)):
        A.append(A2[i])
        b.append(b2[i])
        sign_limits.append("<=")
    return A, b, c, v, sign_limits, type_opt, value_limits
