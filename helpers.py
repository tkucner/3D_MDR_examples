import numpy as np


def divide_cube(cube):
    x_mid = cube['x_min'] + (cube['x_max'] - cube['x_min']) / 2
    y_mid = cube['y_min'] + (cube['y_max'] - cube['y_min']) / 2
    z_mid = cube['z_min'] + (cube['z_max'] - cube['z_min']) / 2
    cubes = {0: {'x_min': cube['x_min'], 'y_min': cube['y_min'], 'z_min': cube['z_min'], 'x_max': x_mid, 'y_max': y_mid,
                 'z_max': z_mid},
             1: {'x_min': x_mid, 'y_min': cube['y_min'], 'z_min': cube['z_min'], 'x_max': cube['x_max'], 'y_max': y_mid,
                 'z_max': z_mid},
             2: {'x_min': cube['x_min'], 'y_min': y_mid, 'z_min': cube['z_min'], 'x_max': x_mid, 'y_max': cube['y_max'],
                 'z_max': z_mid},
             3: {'x_min': x_mid, 'y_min': y_mid, 'z_min': cube['z_min'], 'x_max': cube['x_max'], 'y_max': cube['y_max'],
                 'z_max': z_mid},
             4: {'x_min': cube['x_min'], 'y_min': cube['y_min'], 'z_min': z_mid, 'x_max': x_mid, 'y_max': y_mid,
                 'z_max': cube['z_max']},
             5: {'x_min': x_mid, 'y_min': cube['y_min'], 'z_min': z_mid, 'x_max': cube['x_max'], 'y_max': y_mid,
                 'z_max': cube['z_max']},
             6: {'x_min': cube['x_min'], 'y_min': y_mid, 'z_min': z_mid, 'x_max': x_mid, 'y_max': cube['y_max'],
                 'z_max': cube['z_max']},
             7: {'x_min': x_mid, 'y_min': y_mid, 'z_min': z_mid, 'x_max': cube['x_max'], 'y_max': cube['y_max'],
                 'z_max': cube['z_max']}}
    return cubes


def in_cube(points, cube):
    x = np.array([item[0] for item in points])
    y = np.array([item[1] for item in points])
    z = np.array([item[2] for item in points])
    x_flag = np.logical_and(x >= cube['x_min'], x < cube['x_max'])
    y_flag = np.logical_and(y >= cube['y_min'], y < cube['y_max'])
    z_flag = np.logical_and(z >= cube['z_min'], z < cube['z_max'])
    flag = np.logical_and(np.logical_and(x_flag, y_flag), z_flag)
    points_in = []
    for point, flag in zip(points, flag):
        if flag:
            points_in.append(point)
    return points_in, len(points_in)


def compute_max_cube(points):
    cm = [np.mean([item[0] for item in points]), np.mean([item[1] for item in points]),
          np.mean([item[2] for item in points])]
    max_dim = np.abs(max([item[0] for item in points]) - cm[0])
    max_dim = max(np.abs(min([item[0] for item in points]) - cm[0]), max_dim)
    max_dim = max(np.abs(max([item[1] for item in points]) - cm[1]), max_dim)
    max_dim = max(np.abs(min([item[1] for item in points]) - cm[1]), max_dim)
    max_dim = max(np.abs(max([item[2] for item in points]) - cm[2]), max_dim)
    max_dim = max(np.abs(min([item[2] for item in points]) - cm[2]), max_dim)
    cube = {'x_max': cm[0] + max_dim, 'x_min': cm[0] - max_dim, 'y_max': cm[1] + max_dim, 'y_min': cm[1] - max_dim,
            'z_max': cm[2] + max_dim, 'z_min': cm[2] - max_dim}
    return cube
