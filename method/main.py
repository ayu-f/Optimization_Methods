from transport_problem import TransportProblem
from input import input_

def main():
    """c = [[8, 9, 7, 5], [5, 6, 4, 4], [7, 8, 7, 7], [5, 2, 1, 1], [4, 3, 4, 2]]
    a = [11, 15, 10, 10]
    b = [11, 8, 10, 9, 8]"""
    A, B, C = input_("tproblem.txt")

    t = TransportProblem(C, A, B)
    t.solve()



main()