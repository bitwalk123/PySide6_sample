# Reference:
# https://stackoverflow.com/questions/58186783/updating-matplotlib-figures-in-real-time-for-data-acquisition
import matplotlib.pyplot as plt
import numpy

if __name__ == '__main__':
    x_max = 500

    fig = plt.figure()
    ax = fig.gca()
    ax.set_xlim(0, x_max)
    ax.set_ylim(-1, 1)
    plt.grid()

    line, = plt.plot([], [])
    for i in range(x_max):
        x = float(i)
        y = numpy.sin(x * 0.1)

        line.set_xdata(numpy.append(line.get_xdata(), [x]))
        line.set_ydata(numpy.append(line.get_ydata(), [y]))

        fig.canvas.draw_idle()
        fig.canvas.flush_events()

        # adjust pause duration here
        plt.pause(0.01)

    print("DONE")
    plt.show()
