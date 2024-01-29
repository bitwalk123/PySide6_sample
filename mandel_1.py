# Reference:
# https://qiita.com/jabberwocky0139/items/33add5b3725204ad377f
import numpy as np
import matplotlib.pyplot as plt

N, M = 50, 500


def mandel(X, Y):
    a, b = [0] * 2
    for i in range(N):
        a, b = a ** 2 - b ** 2 + X, 2 * a * b + Y

    return a ** 2 + b ** 2 < 4


if __name__ == '__main__':
    x, y = [np.linspace(-2, 2, M)] * 2
    X, Y = np.meshgrid(x, y)
    plt.pcolor(X, Y, mandel(X, Y))
    plt.show()
