def input_general_f(filename: str):
    file = open(filename, "r")
    n = int(file.readline())
    signed_indexes = [int(x) for x in
                      file.readline().split()]
    for i in signed_indexes:
        if i not in range(n):
            raise Exception("Invalid input")
    type = file.readline().split()[0]
    if type != "min" and type != "max":
        raise Exception("Invalid input")
    c1 = [float(x) for x in file.readline().split()]
    m1 = int(file.readline())
    b1 = [0. for i in range(m1)]
    A1 = [[0. for i in range(n)] for j in range(m1)]
    for j in range(m1):
        line = file.readline()
        data = [float(x) for x in line.split()]
        if len(data) != n + 1:
            raise Exception("Invalid input")
        for i in range(n):
            A1[j][i] = data[i]
        b1[j] = data[n]

    m2 = int(file.readline())
    b2 = [0. for i in range(m2)]
    A2 = [[0. for i in range(n)] for j in range(m2)]
    for j in range(m2):
        line = file.readline()
        data = [float(x) for x in line.split()]
        if len(data) != n + 1:
            raise Exception("Invalid input")
        for i in range(n):
            A2[j][i] = data[i]
        b2[j] = data[n]

    m3 = int(file.readline())
    b3 = [0. for i in range(m3)]
    A3 = [[0. for i in range(n)] for j in range(m3)]
    for j in range(m3):
        line = file.readline()
        data = [float(x) for x in line.split()]
        if len(data) != n + 1:
            raise Exception("Invalid input")
        for i in range(n):
            A3[j][i] = data[i]
        b3[j] = data[n]

    return signed_indexes, c1, type, A1, b1, A2, b2, A3, b3


def input_general():
    n = int(input("Введите число переменных задачи: "))
    signed_indexes = [int(x) for x in input("Введите номера переменных для которых введено положительное ограничение на знак:").split()]
    for i in signed_indexes:
        if i not in range(n):
            print("Некоректный индекс.")
            raise Exception("Invalid input")
    type = input("Введите тип задачи (min или max): ")
    if type != "min" and type != "max":
        raise Exception("Invalid input")
    c1 = [float(x) for x in input("Введите коэффициенты линейной функции цели: ").split()]
    m1 = int(input("Введите число линейных ограничений с равенством: "))
    b1 = [0. for i in range(m1)]
    A1 = [[0. for i in range(n)] for j in range(m1)]
    for j in range(m1):
        line = input("Введите коэффициенты ограничения: ")
        data = [float(x) for x in line.split()]
        if len(data) != n + 1:
            raise Exception("Invalid input")
        for i in range(n):
            A1[j][i] = data[i]
        b1[j] = data[n]

    m2 = int(input("Введите число линейных ограничений с >=: "))
    b2 = [0. for i in range(m2)]
    A2 = [[0. for i in range(n)] for j in range(m2)]
    for j in range(m2):
        line = input("Введите коэффициенты ограничения: ")
        data = [float(x) for x in line.split()]
        if len(data) != n + 1:
            raise Exception("Invalid input")
        for i in range(n):
            A2[j][i] = data[i]
        b2[j] = data[n]

    m3 = int(input("Введите число линейных ограничений с <=: "))
    b3 = [0. for i in range(m3)]
    A3 = [[0. for i in range(n)] for j in range(m3)]
    for j in range(m3):
        line = input("Введите коэффициенты ограничения: ")
        data = [float(x) for x in line.split()]
        if len(data) != n + 1:
            raise Exception("Invalid input")
        for i in range(n):
            A3[j][i] = data[i]
        b3[j] = data[n]

    return signed_indexes, c1, type, A1, b1, A2, b2, A3, b3



