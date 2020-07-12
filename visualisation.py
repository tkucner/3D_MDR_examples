import matplotlib.colors as cs
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

import helpers as he


def expand_coordinates(indices):
    x, y, z = indices
    x[1::2, :, :] += 1
    y[:, 1::2, :] += 1
    z[:, :, 1::2] += 1
    return x, y, z


def to_hex_wrapper(c):
    return cs.to_hex(c, keep_alpha=True)


def explode(data):
    shape_arr = np.array(data.shape)
    size = shape_arr[:3] * 2 - 1
    exploded = np.zeros(np.concatenate([size, shape_arr[3:]]), dtype=data.dtype)
    exploded[::2, ::2, ::2] = data
    return exploded


def make_ax(grid=False):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.grid(grid)
    return ax


def rect_prism(x_range, y_range, z_range, ax, color="r"):
    xx, yy = np.meshgrid(x_range, y_range)
    ax.plot_wireframe(xx, yy, z_range[0] * np.ones(yy.shape), color=color)
    ax.plot_surface(xx, yy, z_range[0] * np.ones(yy.shape), color=color, alpha=0.2)
    ax.plot_wireframe(xx, yy, z_range[1] * np.ones(yy.shape), color=color)
    ax.plot_surface(xx, yy, z_range[1] * np.ones(yy.shape), color=color, alpha=0.2)

    yy, zz = np.meshgrid(y_range, z_range)
    ax.plot_wireframe(x_range[0], yy, zz, color=color)
    ax.plot_surface(x_range[0], yy, zz, color=color, alpha=0.2)
    ax.plot_wireframe(x_range[1], yy, zz, color=color)
    ax.plot_surface(x_range[1], yy, zz, color=color, alpha=0.2)

    xx, zz = np.meshgrid(x_range, z_range)
    ax.plot_wireframe(xx, y_range[0], zz, color=color)
    ax.plot_surface(xx, y_range[0], zz, color=color, alpha=0.2)
    ax.plot_wireframe(xx, y_range[1], zz, color=color)
    ax.plot_surface(xx, y_range[1], zz, color=color, alpha=0.2)


def show_oct_tree(tree):
    ax = make_ax()
    for node in tree:
        if node.leaf:
            if len(node.points) > 0:
                rect_prism(np.array([node.corners['x_min'], node.corners['x_max']]),
                           np.array([node.corners['y_min'], node.corners['y_max']]),
                           np.array([node.corners['z_min'], node.corners['z_max']]), ax, "r")
            else:
                rect_prism(np.array([node.corners['x_min'], node.corners['x_max']]),
                           np.array([node.corners['y_min'], node.corners['y_max']]),
                           np.array([node.corners['z_min'], node.corners['z_max']]), ax, "b")

    plt.show()


def show_pseudo_measurements(pseudo_walls):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for pw in pseudo_walls:
        x = [pw['par']['a'][0], pw['par']['b'][0], pw['par']['c'][0], pw['par']['d'][0], pw['par']['a'][0]]
        y = [pw['par']['a'][1], pw['par']['b'][1], pw['par']['c'][1], pw['par']['d'][1], pw['par']['a'][1]]
        z = [pw['par']['a'][2], pw['par']['b'][2], pw['par']['c'][2], pw['par']['d'][2], pw['par']['a'][2]]
        ax.plot(x, y, z)
        ax.plot([item[0] for item in pw['points']], [item[1] for item in pw['points']],
                [item[2] for item in pw['points']], '.')

    plt.show()


def show_pseudo_dense_grid(h):
    ax = make_ax()

    alpha = np.expand_dims(h / h.max(), axis=3)
    colors = np.array([[[[0.12, 0.46, 0.7]] * alpha.shape[2]] * alpha.shape[1]] * alpha.shape[0])
    colors = np.append(colors, alpha, axis=3)
    colors = np.apply_along_axis(to_hex_wrapper, 3, colors)

    filled = explode(np.ones(colors.shape))
    colors = explode(colors)

    x, y, z = expand_coordinates(np.indices(np.array(filled.shape) + 1))
    ax.voxels(x, y, z, filled, facecolors=colors, edgecolors='#80808001', shade=False)
    plt.show()


def show_pseudo_sparse_grid(sparse):
    ax = make_ax()
    for cell in sparse.elements:
        rect_prism(np.array([cell[0], cell[0] + 1]), np.array([cell[1], cell[1] + 1]), np.array([cell[2], cell[2] + 1]),
                   ax, "r")
    plt.show()


def show_pseudo_pointcloud(points):
    ax = make_ax()
    ax.plot([item[0] for item in points], [item[1] for item in points], [item[2] for item in points], '.')
    plt.show()


def show_pseudo_mesh(mesh):
    ax = make_ax()

    x_min = float('Inf')
    x_max = -float('Inf')
    y_min = float('Inf')
    y_max = -float('Inf')
    z_min = float('Inf')
    z_max = -float('Inf')

    verts = []
    for pw in mesh:
        x, y, z = he.get_points_from_mesh(pw)
        x_min = min(x_min, min(x))
        x_max = max(x_max, max(x))
        y_min = min(y_min, min(y))
        y_max = max(y_max, max(y))
        z_min = min(z_min, min(z))
        z_max = max(z_max, max(z))

        verts.append(list(zip(x, y, z)))

    poly = Poly3DCollection(verts, alpha=.6)

    ax.set_xlim3d(x_min, x_max)
    ax.set_ylim3d(y_min, y_max)
    ax.set_zlim3d(z_min, z_max)

    ax.add_collection3d(poly)

    plt.show()
