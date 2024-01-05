# Reference:
# https://matplotlib.org/stable/gallery/mplot3d/subplot3d.html#sphx-glr-gallery-mplot3d-subplot3d-py
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

X = np.arange(-5, 5, 0.25)
Y = np.arange(-5, 5, 0.25)
X, Y = np.meshgrid(X, Y)
R = np.sqrt(X ** 2 + Y ** 2)
Z = np.sin(R)

fig, ax = plt.subplots(subplot_kw={'projection': '3d'})
surf = ax.plot_surface(
    X, Y, Z,
    rstride=1, cstride=1,
    cmap=mpl.colormaps['coolwarm'],
    linewidth=0, antialiased=False
)
ax.set_zlim(-1.01, 1.01)
fig.colorbar(surf, shrink=0.5, aspect=10)

plt.show()
