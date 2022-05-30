import copy
import math

import numpy as np
import matplotlib.pyplot as plt
from numpy import ndarray


def func1(x, y):
    return 2 * (x ** 2) + (y ** 2) + x * y


def grad1(x, y):
    return np.array([4 * x + y, 2 * y + x])


def hessian1(x, y):
    return np.array([[4, 1], [1, 2]])


optimum1 = [0., 0.]


def func2(x, y):
    return (x / 1) ** 4 + (y / 2) ** 4


def grad2(x, y):
    return np.array([
        4 * (x ** 3),
        (1 / 4) * (y ** 3)]
    )


def hessian2(x, y):
    return np.array([
        [
            12 * (x ** 2),
            0
        ],
        [
            0,
            (3 / 4) * (y ** 2),
        ]
    ])


optimum2 = [0., 0.]


def func3(x, y):
    return (x/1)**4+(y/2)**4+(x/2)**2+(y/1)**2


def grad3(x, y):
    return np.array([
        4 * (x**3) + x/2,
        (y**3)/4 + 2*y]
    )


def hessian3(x, y):
    return np.array([
        [
            12 * (x**2) + 1/2,
            0
        ],
        [
            0,
            3*(y**2)/4 + 2,
        ]
    ])


optimum3 = [0., 0.]


def func4(x, y):
    return (x**(2))+(y**(2))+0.005*((x**(4))+(y**(4)))+0.00025*((x**(6))+(y**(6)))+5*(x+y)


def grad4(x, y):
    return np.array([
        0.0015*(x**5) + 0.02*(x**3) + 2*x + 5,
        0.0015*(y**5) + 0.02*(y**3) + 2*y + 5]
    )


def hessian4(x, y):
    return np.array([
        [
            0.0075*(x**4) + 0.6*(x**2) + 2,
            0
        ],
        [
            0,
            0.0075*(y**4) + 0.6*(y**2) + 2,
        ]
    ])


optimum4 = [-2.323714531621294149745910231, -2.323714531621294149745910231]


functions = (
    {
        "name": "func1",
        "label": "$f_1(x, y) = 2x^2 + y^2 + xy$",
        "func": func1,
        "grad": grad1,
        "hessian": hessian1,
        "optimum": optimum1,
        "init_point": [1.1, 1.1],
        "range_x": [-2, 2],
        "range_y": [-2, 2],
    },
    {
        "name": "func2",
        "label": "$f_2(x, y) = x^4 + (\\frac{y}{2})^4$",
        "func": func2,
        "grad": grad2,
        "hessian": hessian2,
        "optimum": optimum2,
        "init_point": [1, 3],
        "range_x": [-5, 5],
        "range_y": [-5, 5],
    },
    {
        "name": "func3",
        "label": "$f_3(x, y) = x^4 + (\\frac{y}{2})^4 + (\\frac{x}{2})^2 + y^2$",
        "func": func3,
        "grad": grad3,
        "hessian": hessian3,
        "optimum": optimum3,
        "init_point": [1, 3],
        "range_x": [-5, 5],
        "range_y": [-5, 5],
    },
    {
        "name": "func4",
        "label": "$f_4(x, y) = x^2+y^2+0.005 (x^4+y^4)+0.00025 (x^6+y^6)+5 (x+y)$",
        "func": func4,
        "grad": grad4,
        "hessian": hessian4,
        "optimum": optimum4,
        "init_point": [1, 3],
        "range_x": [-5, 5],
        "range_y": [-5, 5],
    },

)


steps_data = {'origin': [], 'step_vector': [], 'iter_for_step_count': [], 'step_coeff': [], 'level': [], 'accuracy': [], 'final': None, 'known_optimum': None}


def add_step(x, dx, func, i, step):
    steps_data['origin'].append(x)
    steps_data['step_vector'].append(dx)
    steps_data['iter_for_step_count'].append(i)
    steps_data['step_coeff'].append(step)
    steps_data['level'].append(func(x[0], x[1]))
    steps_data['accuracy'].append(math.sqrt(np.dot(np.subtract(x, steps_data['known_optimum']), np.subtract(x, steps_data['known_optimum']))))


def clear_step_data():
    steps_data['origin'] = []
    steps_data['step_vector'] = []
    steps_data['iter_for_step_count'] = []
    steps_data['step_coeff'] = []
    steps_data['level'] = []
    steps_data['accuracy'] = []
    steps_data['final'] = None
    steps_data['known_optimum'] = None


def find_step(x, p, func, precision):
    a = -5.
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


def find_newton_step(grad_y, hessian_y):
    try:
        p = np.linalg.solve(hessian_y, -grad_y)
    except:
        p = -grad_y
    return p


def grad_second_newton(init_x, func, grad, hessian, precision):
    x = init_x
    cur_grad = grad(*x)
    grad_norm_sqr = np.dot(cur_grad, cur_grad)
    k = 0
    while math.sqrt(grad_norm_sqr) > precision:
        p = find_newton_step(cur_grad, hessian(*x))
        a = 1
        s = p * a
        add_step(x, s, func, None, a)
        x = x + s
        cur_grad = grad(*x)
        grad_norm_sqr = np.dot(cur_grad, cur_grad)
        k += 1
        if k > 100:
            break
    return k, x


def fixed_grad_second_newton(init_x, func, grad, hessian, precision):
    known_optimum = steps_data['known_optimum']
    x = init_x
    cur_grad = grad(*x)
    grad_norm_sqr = np.dot(cur_grad, cur_grad)
    k = 0
    while math.sqrt(np.dot(known_optimum-x,known_optimum-x)) > precision:
        p = find_newton_step(cur_grad, hessian(*x))
        a = 1
        s = p * a
        add_step(x, s, func, None, a)
        x = x + s
        cur_grad = grad(*x)
        grad_norm_sqr = np.dot(cur_grad, cur_grad)
        k += 1
        if k > 100:
            break
    return k, x


def grad_second_pshenichnyy(init_x, func, grad, hessian, init_step, split_scale, delta, precision):
    x = init_x
    cur_grad = grad(*x)
    grad_norm_sqr = np.dot(cur_grad, cur_grad)
    k = 0
    while math.sqrt(grad_norm_sqr) > precision:
        p = find_newton_step(cur_grad, hessian(*x))
        a = init_step
        s = p * a
        x_next = x + s
        f_cur = func(*x)
        f_next = func(*x_next)
        i = 0
        while f_next - f_cur > delta * a * grad_norm_sqr:
            a *= split_scale
            s = p * a
            x_next = x + s
            f_next = func(*x_next)
            i += 1
            if i > 100:
                break
        add_step(x, s, func, i, a)
        x = x_next
        cur_grad = grad(*x)
        grad_norm_sqr = np.dot(cur_grad, cur_grad)
        k += 1
        if k > 100:
            break
    return k, x


def fixed_grad_second_pshenichnyy(init_x, func, grad, hessian, init_step, split_scale, delta, precision):
    known_optimum = steps_data['known_optimum']
    x = init_x
    cur_grad = grad(*x)
    grad_norm_sqr = np.dot(cur_grad, cur_grad)
    k = 0
    while math.sqrt(np.dot(known_optimum-x,known_optimum-x)) > precision:
        p = find_newton_step(cur_grad, hessian(*x))
        a = init_step
        s = p * a
        x_next = x + s
        f_cur = func(*x)
        f_next = func(*x_next)
        i = 0
        while f_next - f_cur > delta * a * grad_norm_sqr:
            a *= split_scale
            s = p * a
            x_next = x + s
            f_next = func(*x_next)
            i += 1
            if i > 100:
                break
        add_step(x, s, func, i, a)
        x = x_next
        cur_grad = grad(*x)
        grad_norm_sqr = np.dot(cur_grad, cur_grad)
        k += 1
        if k > 100:
            break
    return k, x


def grad_second_bfgs(init_x, func, grad, precision):
    c = np.eye(len(init_x))
    x = init_x
    cur_grad = grad(*x)
    grad_norm_sqr = np.dot(cur_grad, cur_grad)
    k = 0
    while math.sqrt(grad_norm_sqr) > precision:
        p = np.dot(c, cur_grad)
        a = find_step(x, p, func, precision/10)
        s = p * a
        add_step(x, s, func, None, -a)
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
        if k > 100:
            break
    return k, x


def fixed_grad_second_bfgs(init_x, func, grad, precision):
    known_optimum = steps_data['known_optimum']
    c = np.eye(len(init_x))
    x = init_x
    cur_grad = grad(*x)
    grad_norm_sqr = np.dot(cur_grad, cur_grad)
    k = 0
    while math.sqrt(np.dot(known_optimum-x,known_optimum-x)) > precision:
        p = np.dot(c, cur_grad)
        a = find_step(x, p, func, 0.00001)
        s = p * a
        add_step(x, s, func, None, -a)
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
        if k > 100:
            break
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


def plot_illustration(ax, func, x_range, y_range):
    arrows_origins = np.array(steps_data['origin'])
    arrows_vectors = np.array(steps_data['step_vector'])
    levels = sorted(steps_data['level'])
    i = 0
    while i < len(levels) - 1:
        if levels[i] == levels[i+1]:
            levels.pop(i+1)
        else:
            i += 1
    if level_mode == "GRID":
        grid: list[list, list, list] = [[], [], []]
        grid[0], grid[1] = np.meshgrid(np.linspace(x_range[0], x_range[1], 100), np.linspace(y_range[0], y_range[1], 100))
        grid[2] = np.ndarray((100, 100))
        for i in range(100):
            for j in range(100):
                grid[2][i, j] = func(grid[0][i, j], grid[1][i, j])
        ax.contour(grid[0], grid[1], grid[2], levels=levels)
    elif level_mode == "ANALITIC":
        pass
    ax.quiver(arrows_origins[:, 0], arrows_origins[:, 1], arrows_vectors[:, 0], arrows_vectors[:, 1], angles='xy',
              scale_units='xy', width=.005, scale=1)


def print_step_data():
    origin = steps_data['origin']
    final = steps_data['final']
    iter_for_step_count = steps_data['iter_for_step_count']
    step_coeff = steps_data['step_coeff']
    optimum = steps_data['known_optimum']
    k = len(origin)
    for i in range(k):
        print(f"xk :{origin[i]} ik : {iter_for_step_count[i]} ak : {step_coeff[i]} ")
    for i in range(k - 1):
        norm1 = math.sqrt(np.dot(np.subtract(origin[i], optimum), np.subtract(origin[i], optimum)))
        norm2 = math.sqrt(np.dot(np.subtract(origin[i+1], optimum), np.subtract(origin[i+1], optimum)))
        print(f"qk :{norm2/norm1} ")

    i = k - 1
    norm1 = math.sqrt(np.dot(np.subtract(origin[i], optimum), np.subtract(origin[i], optimum)))
    norm2 = math.sqrt(np.dot(np.subtract(final, optimum), np.subtract(final, optimum)))
    print(f"qk :{norm2/norm1} ")


def plot_accuracy_graph(ax, fmt, **kwargs):
    optimum = steps_data['known_optimum']
    final = steps_data['final']
    origin = steps_data['origin']
    accuracy = copy.copy(steps_data['accuracy'])
    accuracy.append(math.sqrt(np.dot(np.subtract(final, optimum), np.subtract(final, optimum))))
    ax.plot(range(len(origin) + 1), accuracy, fmt, **kwargs)
    s = 2 + 5


def plot_steps_to_accuracy_graph(ax, label, accuracy_list, steps_list):
    steps_mean = []
    for i in range(len(accuracy_list)):
        steps_mean.append(np.mean(steps_data[i]))
    ax.plot(accuracy_list, steps_mean, label=label)




def experiment1():
    acc = 1e-6
    for function in functions:
        max_k = 0
        frfr, ac_fig = plt.subplots(1, 1)
        ac_fig.set_title(function['label'])
        ac_fig.set_yscale('log')
        fig, axes = plt.subplots(1, 3, figsize=(9, 4), gridspec_kw={'left': 0.06, 'right': 0.990, 'bottom': 0.16, 'wspace': 0.3})
        axes[0].set_title('newton')
        clear_step_data()
        steps_data['known_optimum'] = function['optimum']
        k, x = grad_second_newton(function['init_point'], function['func'], function['grad'], function['hessian'], acc)
        steps_data['final'] = x
        print_step_data()
        plot_illustration(axes[0], function['func'], function['range_x'], function['range_y'])
        plot_accuracy_graph(ac_fig, 'r-', label='newton')
        max_k = max(max_k, k)

        axes[1].set_title('pshenichnyy')
        clear_step_data()
        steps_data['known_optimum'] = function['optimum']
        k, x = grad_second_pshenichnyy(function['init_point'], function['func'], function['grad'], function['hessian'], 1.0, 0.9, 0.45, acc)
        steps_data['final'] = x
        print_step_data()
        plot_illustration(axes[1], function['func'], function['range_x'], function['range_y'])
        plot_accuracy_graph(ac_fig, 'k:', label='pshenichnyy', linewidth=3)
        max_k = max(max_k, k)

        axes[2].set_title('bfgs')
        clear_step_data()
        steps_data['known_optimum'] = function['optimum']
        k, x = grad_second_bfgs(function['init_point'], function['func'], function['grad'], acc)
        steps_data['final'] = x
        print_step_data()
        plot_illustration(axes[2], function['func'], function['range_x'], function['range_y'])
        plot_accuracy_graph(ac_fig, 'b-', label='bfgs')
        max_k = max(max_k, k)
        ac_fig.plot([0, max_k], [acc, acc], 'g--')
        ac_fig.legend()
        frfr.savefig("../course_paper/figures/acc_from_step_" + function['name'] + ".png")
        fig.savefig("../course_paper/figures/process_view_" + function['name'] + ".png")



def experiment2():
    sample_size = 100
    for function in functions:
        acc = 1e-6
        fig, ac_fig = plt.subplots(1, 1)
        ac_fig.set_title(function['label'])
        ac_fig.set_yscale('log')
        init_range = 2
        max_k = 0
        steps_list = [[], []]
        final_acc_list = [[], []]
        for i in range(sample_size):
            angle = 2 * np.pi / sample_size * i
            init_point = function['optimum'] + init_range * (np.array([np.sin(angle), np.cos(angle)]))

            clear_step_data()
            steps_data['known_optimum'] = function['optimum']
            k, x = fixed_grad_second_newton(init_point, function['func'], function['grad'], function['hessian'], acc)
            steps_data['final'] = x
            plot_accuracy_graph(ac_fig, 'r-', alpha=20 / sample_size)
            max_k = max(max_k, k)
            steps_list[0].append(k)
            final_acc_list[0].append(x)

            clear_step_data()
            steps_data['known_optimum'] = function['optimum']
            k, x = fixed_grad_second_bfgs(init_point, function['func'], function['grad'], acc)
            steps_data['final'] = x
            plot_accuracy_graph(ac_fig, 'b-', alpha=20/sample_size)
            max_k = max(max_k, k)
            steps_list[1].append(k)
            final_acc_list[1].append(x)
        print('{} newton: k_mean = {}'.format(function['name'], np.mean(steps_list[0])))
        print('{} bfgs: k_mean = {}'.format(function['name'], np.mean(steps_list[1])))
        ac_fig.plot([0, max_k], [acc, acc], 'g--')
        fig.savefig("../course_paper/figures/init_100_" + function['name'] + ".png")






def main():
    experiment1()
    experiment2()


if __name__ == '__main__':
    main()

