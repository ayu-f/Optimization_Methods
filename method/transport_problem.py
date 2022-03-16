import copy
import method.recalc_cycle

class TransportProblem:
    direction = [[-1, 0], [0, 1], [0, -1], [1, 0]]

    def __init__(self, c: list, a: list, b: list):
        self.a = copy.deepcopy(a)
        self.b = copy.deepcopy(b)
        self.u = [None for i in range(len(a))]
        self.v = [None for i in range(len(b))]
        # kk = c[4][0]
        self.c = [[c[j][i] for i in range(len(b))] for j in range(len(a))]
        self.delta_c = [[c[j][i] for i in range(len(b))] for j in range(len(a))]
        self.bs_tab = [[None for i in range(len(b))] for j in range(len(a))]

    def is_optimal(self):
        ans = True
        i_start = -1
        j_start = -1
        for i in range(0, len(self.a)):
            for j in range(0, len(self.b)):
                if self.bs_tab[i][j] is None:
                    self.delta_c[i][j] = self.c[i][j] - self.u[i] - self.v[j]
                    if self.delta_c[i][j] < 0:
                        ans = False
                        if i_start == -1 or abs(self.delta_c[i][j]) > abs(self.delta_c[i_start][j_start]):
                            i_start = i
                            j_start = j

        return ans, i_start, j_start  # indexes of minimal element in delta c

    def northwest_corn(self):
        a = copy.deepcopy(self.a)
        b = copy.deepcopy(self.b)
        i = 0
        j = 0
        steps = 0
        while i != len(a) and j != len(b):
            min_v = min(a[i], b[j])
            a[i] -= min_v
            b[j] -= min_v
            self.bs_tab[i][j] = min_v
            if a[i] == 0:
                i += 1
            if b[j] == 0:
                j += 1
            steps += 1

        if steps != len(a) + len(b) - 1:
            # self.bs_tab[0][1] = 0
            for i in range(len(self.bs_tab)):
                for j in range(len(self.bs_tab[0])):
                    if self.bs_tab[i][j] is None:
                        self.bs_tab[i][j] = 0
                        return

    def potential_method(self):
        self.v = [None for i in self.v]
        self.u = [None for i in self.u]
        self.u[0] = 0
        u_idx = []
        v_idx = []
        slau = []
        for i in range(0, len(self.c)):
            for j in range(0, len(self.c[0])):
                if self.bs_tab[i][j] is not None:
                    slau.append([i, j])

        while True:
            for eq in slau:
                i = eq[0]
                j = eq[1]
                if self.u[i] is not None:
                    self.v[j] = self.c[i][j] - self.u[i]
                    slau.remove(eq)
                elif self.v[j] is not None:
                    self.u[i] = self.c[i][j] - self.v[j]
                    slau.remove(eq)
            if len(slau) == 0:
                return

    def print_plan(self):
        for row in self.bs_tab:
            for c in range(len(row)):
                s = "*" if row[c] is None else row[c]
                print(s, end=", ")
            print()

    def print_potential(self):
        for i in range(len(self.u)):
            print(f'u_{i} = {self.u[i]}', end="; ")
        print()
        for i in range(len(self.v)):
            print(f'v_{i} = {self.v[i]}', end="; ")
        print()

    def print_info(self, i: int, j: int):
        print("Новый план:")
        self.print_plan()
        self.print_potential()
        if i != -1:
            print(f"Рабочая точка: {i, j}")
        print(f"Значение: {self.calc_func()}\n")

    def calc_func(self):
        result = 0
        for i in range(len(self.bs_tab)):
            for j in range(len(self.bs_tab[0])):
                if self.bs_tab[i][j] is not None:
                    result += self.bs_tab[i][j] * self.c[i][j]
        return result

    def solve(self):
        self.northwest_corn()
        self.potential_method()
        is_optimal, i, j = self.is_optimal()
        print("Стартовый план:")
        self.print_plan()
        self.print_potential()
        print(f"Рабочая точка: {i, j}")
        print(f"Значение: {self.calc_func()}\n")
        while not is_optimal:
            # self.recalc_cycle(self.Point(i, j), self.Point(i, j))
            self.bs_tab = method.recalc_cycle.change_plan(self.bs_tab, [i, j])
            self.potential_method()
            is_optimal, i, j = self.is_optimal()
            self.print_info(i, j)

