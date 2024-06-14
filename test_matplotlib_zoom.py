# Reference:
# https://stackoverflow.com/questions/48474699/marker-size-alpha-scaling-with-window-size-zoom-in-plot-scatter
from matplotlib import pyplot as plt
import numpy as np

fig, axes = plt.subplots(nrows=1, ncols=2)
ax1, ax2 = axes
fig_width = fig.get_figwidth()
fig_height = fig.get_figheight()
fig_factor = 1.0

##saving some values
xlim = dict()
ylim = dict()
lines = dict()
line_sizes = dict()
paths = dict()
point_sizes = dict()

## a line plot
x1 = np.linspace(0, np.pi, 30)
y1 = np.sin(x1)

lines[ax1] = ax1.plot(x1, y1, 'ro', markersize=3, alpha=0.8)
xlim[ax1] = ax1.get_xlim()
ylim[ax1] = ax1.get_ylim()
line_sizes[ax1] = [line.get_markersize() for line in lines[ax1]]

## a scatter plot
x2 = np.random.normal(1, 1, 30)
y2 = np.random.normal(1, 1, 30)

paths[ax2] = ax2.scatter(x2, y2, c='b', s=20, alpha=0.6)
point_sizes[ax2] = paths[ax2].get_sizes()

xlim[ax2] = ax2.get_xlim()
ylim[ax2] = ax2.get_ylim()


def on_resize(event):
    global fig_factor

    w = fig.get_figwidth()
    h = fig.get_figheight()

    fig_factor = min(w / fig_width, h / fig_height)

    for ax in axes:
        lim_change(ax)


def lim_change(ax):
    lx = ax.get_xlim()
    ly = ax.get_ylim()

    factor = min(
        (xlim[ax][1] - xlim[ax][0]) / (lx[1] - lx[0]),
        (ylim[ax][1] - ylim[ax][0]) / (ly[1] - ly[0])
    )

    try:
        for line, size in zip(lines[ax], line_sizes[ax]):
            line.set_markersize(size * factor * fig_factor)
    except KeyError:
        pass

    try:
        paths[ax].set_sizes([s * factor * fig_factor for s in point_sizes[ax]])
    except KeyError:
        pass


fig.canvas.mpl_connect('resize_event', on_resize)
for ax in axes:
    ax.callbacks.connect('xlim_changed', lim_change)
    ax.callbacks.connect('ylim_changed', lim_change)
plt.show()
