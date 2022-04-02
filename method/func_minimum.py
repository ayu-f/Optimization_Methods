import math


class Searcher:
    def __init__(self, func):
        self.func = func

    def golden_section(self, a: float, b: float, eps: float) -> [float, int]:

        phi = (1 + math.sqrt(5)) / 2
        rphi = 2 - phi
        x1 = a + rphi * (b - a)
        x2 = b - rphi * (b - a)
        f1 = self.func(x1)
        f2 = self.func(x2)
        count_of_calls_func = 2

        while math.fabs(b - a) > eps:
            if f1 < f2:
                b = x2
                x2 = x1
                f2 = f1
                x1 = a + rphi * (b - a)
                f1 = self.func(x1)
            else:
                a = x1
                x1 = x2
                f1 = f2
                x2 = b - rphi * (b - a)
                f2 = self.func(x2)
            count_of_calls_func += 1

        return (x1 + x2) / 2, count_of_calls_func

    def dichotomy_method(self, a: float, b: float, eps: float) -> [float, int]:
        if self.func(a) * self.func(b) > 0:
            raise Exception("f(a)*f(b) should be greater then zero")

        count_of_calls_func = 0
        mid = (b + a) / 2
        delta = (b - a) / 100
        while abs(b - a) > eps:
            mid = (a + b) / 2
            if self.func(mid - delta) < self.func(mid + delta):
                b = mid
            else:
                a = mid
            count_of_calls_func += 2

        return (a + b) / 2, count_of_calls_func

    def th_count_calls_dichotomy(self, a: float, b: float, eps: float) -> int:
        delta = (b - a) / 100
        return math.ceil(abs((math.log2((b - a - delta) / (2*eps)) + 1))) * 2

    def th_count_calls_golden(self, a: float, b: float, eps: float) -> int:
        pass
