from func_minimum import Searcher

def func(x):
    return x**4 + 2 * x**2 + 4 * x + 1  # x^4 +2x^2 +4x + 1


def main():
    eps = [0.1, 0.01, 0.001]
    a = -1
    b = 0
    searcher = Searcher(func)
    print("**** GOLDEN SELECTION ****")
    for i in range(len(eps)):
        ans, count_calls = searcher.golden_section(a, b, eps[i])
        print(f'x = {round(ans, i + 2)}')
        print(f'f(x) =  {round(func(ans), i + 2)}')
        print(f'Count of function calls: {count_calls}')
        print(f'Theoretical count of function calls: PASS')

    print("\n\n**** DICHOTOMY METHOD ****")
    for i in range(len(eps)):
        ans, count_calls = searcher.dichotomy_method(a, b, eps[i])
        print(f'x = {round(ans, i + 2)}')
        print(f'f(x) =  {round(func(ans), i + 2)}')
        print(f'Count of function calls: {count_calls}')
        print(f'Theoretical count of function calls: {searcher.th_count_calls_dichotomy(a, b, eps[i])}')


main()