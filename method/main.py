import math

import numpy as np
import matplotlib.pyplot as plt
from numpy import ndarray


def func1(x1, x2):
    return 2 * x1 * x1 + x2 * x2 + x1 * x2 + x1 + x2


def grad1(x1, x2):
    return np.array([4 * x1 + x2 + 1, 2 * x2 + x1 + 1])


levels = []
arrows = []


def add_step(x, dx, func, i, step):
    levels.append(func(x[0], x[1]))
    arrows.append((x, dx, i, step))


def find_step(x, p, func, precision):
    a = -20.
    b = 0.
    x = np.array(x)
    while b - a > precision:
        c = a + (b - a) / 2.
        f = func(*(x + c * p))
        c_1 = c - precision / 4.
        c_2 = c + precision / 4.
        f_1 = func(*(x + c_1 * p))
        f_2 = func(*(x + c_2 * p))
        if f < f_1 and f < f_2:
            return c
        if f_1 < f_2:
            b = c
        else:
            a = c
    return a




def grad_second_bfgs(init_x, func, grad, precision):
    c = np.eye(len(init_x))
    x = init_x
    cur_grad = grad(*x)
    grad_norm_sqr = np.dot(cur_grad, cur_grad)
    k = 0
    while math.sqrt(grad_norm_sqr) > precision:
        p = np.dot(c, cur_grad)
        a = find_step(x, p, func, 0.00001)
        s = p * a
        # add_step(x, s, func)
        x = x + s
        new_grad = grad(*x)
        y = new_grad - cur_grad
        cur_grad = new_grad
        grad_norm_sqr = np.dot(cur_grad, cur_grad)
        if k % 1 == 0:
            q = 1 / np.dot(y, s)
            c1 = np.outer(s, y)
            c1 *= -q
            c1 += np.eye(len(init_x))
            c2 = np.outer(y, s)
            c2 *= -q
            c2 += np.eye(len(init_x))
            c3 = np.outer(s, s)
            c3 *= q

            c1.dot(c)
            c1.dot(c2)

            c1 += c3

            c = c1
        k += 1
    return k, x


def grad_first_split(init_x, func, grad, init_step, split_scale, delta, precision):
    x = init_x
    cur_grad = grad(*x)
    grad_norm_sqr = np.dot(cur_grad, cur_grad)
    k = 0
    while math.sqrt(grad_norm_sqr) > precision:
        step = init_step
        x_next = x - step * cur_grad
        f_cur = func(*x)
        f_next = func(*x_next)
        i = 0
        while f_next - f_cur > -delta * step * grad_norm_sqr:
            step *= split_scale
            x_next = x - step * cur_grad
            f_next = func(*x_next)
            i += 1
        add_step(x, -step * cur_grad, func, i, step)
        x = x_next
        cur_grad = grad(*x)
        grad_norm_sqr = np.dot(cur_grad, cur_grad)
        k += 1
    return k, x


level_mode = "GRID"


def plot_illustration(ax):
    arrows_array = np.array(arrows)
    if level_mode == "GRID":
        levels.sort()
        grid: list[list, list, list] = [[], [], []]
        grid[0], grid[1] = np.meshgrid(np.linspace(-1, 1, 1000), np.linspace(-1, 1, 1000))
        grid[2] = func1(*(grid[0:2]))
        ax.contour(grid[0], grid[1], grid[2], levels=levels)
    elif level_mode == "ANALITIC":
        pass
    ax.quiver(arrows_array[:, 0, 0], arrows_array[:, 0, 1], arrows_array[:, 1, 0], arrows_array[:, 1, 1], angles='xy',
              scale_units='xy', width=.005, scale=1)


optimum = [-1./7., -3./7.]


def main():
    fig = plt.figure()
    ax = fig.add_subplot(1, 2, 1)
    arrows.clear()
    levels.clear()
    k, x = grad_first_split([-0.1, -0.1], func1, grad1, 0.95, 0.5, 0.3, 1e-8)

    for ar in arrows:
        print(f"xk :{ar[0]} ik : {ar[2]} ak : {ar[3]} ")
    for i in range(len(arrows) - 1):
        norm1 = math.sqrt(np.dot(np.subtract(arrows[i][0], optimum), np.subtract(arrows[i][0], optimum)))
        norm2 = math.sqrt(np.dot(np.subtract(arrows[i+1][0], optimum), np.subtract(arrows[i+1][0], optimum)))
        print(f"qk :{norm2/norm1} ")

    i = len(arrows) - 1
    norm1 = math.sqrt(np.dot(np.subtract(arrows[i][0], optimum), np.subtract(arrows[i][0], optimum)))
    norm2 = math.sqrt(np.dot(np.subtract(x, optimum), np.subtract(x, optimum)))
    print(f"qk :{norm2/norm1} ")




    plt.show()


if __name__ == '__main__':
    main()

