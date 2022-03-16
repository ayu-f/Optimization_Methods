def input_(filename: str):
    with open("../"+filename, 'r') as fp:
        str = fp.readline()
        A_list = str.split(' ')
        A_list = [int(x) for x in A_list]
        str = fp.readline()
        B_list = str.split(' ')
        B_list = [int(x) for x in B_list]
        C_list = []
        for n, line in enumerate(fp, 1):
            str = line.rstrip('\n')
            if (str[0] == '#'):
                continue
            arr = str.split(' ')
            arr = [int(x) for x in arr]
            C_list.append(arr)

        return A_list, B_list, C_list
