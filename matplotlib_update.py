# Reference:
# https://stackoverflow.com/questions/58186783/updating-matplotlib-figures-in-real-time-for-data-acquisition
from math import sin

import matplotlib.pyplot as plt
import numpy

if __name__ == '__main__':
    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim(0, 500)
    ax.set_ylim(-1, 1)

    line, = plt.plot([], [])

    i = 1
    while i < 500:
        x = float(i)
        y = sin(x * 0.1)

        line.set_xdata(numpy.append(line.get_xdata(), [x]))
        line.set_ydata(numpy.append(line.get_ydata(), [y]))

        fig.canvas.draw_idle()
        fig.canvas.flush_events()

        # adjust pause duration here
        plt.pause(0.01)
        i += 1
    else:
        print("DONE")

    plt.show()
