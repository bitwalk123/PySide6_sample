# Reference:
# https://alan-turing-institute.github.io/rse-course/html/module09_programming_for_speed/09_00_performance_programming.html
import matplotlib.pyplot as plt

# we need some complex starting points
xmin = -3
ymin = -3
xmax = 3
ymax = 3
resolution = 300
xstep = (xmax - xmin) / resolution
ystep = (ymax - ymin) / resolution
xs = [(xmin + xstep * i) for i in range(resolution)]
ys = [(ymin + ystep * i) for i in range(resolution)]


def mandel(constant, max_iterations=50):
    """Computes the values of the series for up to a maximum number of iterations.

    The function stops when the absolute value of the series surpasses 2 or when it reaches the maximum
    number of iterations.

    Returns the number of iterations.
    """

    value = 0

    counter = 0
    while counter < max_iterations:
        if abs(value) > 2:
            break

        value = (value ** 2) + constant

        counter = counter + 1

    return counter


if __name__ == '__main__':
    plt.xlabel("Real")
    plt.ylabel("Imaginary")
    plt.imshow(
        [[mandel(x + y * 1j) for x in xs] for y in ys],
        interpolation="none",
        extent=[xmin, xmax, ymin, ymax],
        origin="lower",
    )
    plt.colorbar()
    plt.show()
