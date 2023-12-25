from math import cos
from numpy import arange, vectorize
from matplotlib import pyplot as plt
import json
import os


# Вариант 15

A = -0.25
x_start = -10.0
x_end = 10.0
x_step = 0.01


def f(x):
    st1 = 0
    st2 = 0
    for i in range(1, 6):
        st1 = st1 + (i * cos((i+1) * x + 1))
        for j in range(1, 6):
            st2 = st2 + (i * cos((i+1) * A + 1))
    return st1 * st2


x_arrays = arange(x_start, x_end, x_step)
f2 = vectorize(f)
y_arrays = f2(x_arrays)

plt.plot(x_arrays, y_arrays)
plt.show()

if not os.path.isdir('result'):
    os.mkdir('result')
else:
    print('Уже есть такая директрория')

data = {
    "x: ": x_arrays.tolist(),
    "y: ": y_arrays.tolist()
}


with open('result/data.json', 'w') as file:
    file.write(json.dumps(data, indent=1))


# with open('result/data.json', 'w') as file:
#     result_dir = {'data': []}
#     [result_dir['data'].append({'x': x, 'y': y}) for x, y in zip(x_arrays, y_arrays)]
#     file.write(json.dumps(result_dir, indent=4))
