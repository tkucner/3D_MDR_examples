import argparse
import csv
import math
import random

import numpy as np

import helpers as he
import json_helpers as jh
import nd_sparse_matrix as sp
import visualisation as vis

map_types = ['dense_grid', 'sparse_grid', 'oct_map', 'mesh', 'all']
output_types = ['json', 'plot', 'all']


def check_map_type(value):
    value = value.lower()
    if value not in map_types:
        raise argparse.ArgumentTypeError("%s is an invalid map type" % value)
    return value


def check_output_type(value):
    value = value.lower()
    if value not in output_types:
        raise argparse.ArgumentTypeError("%s is an invalid output type" % value)
    return value


def generate_parallelograms(file):
    with open(file, newline='') as csvfile:
        input_vertices = list(csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC))

    walls = []
    for iv in input_vertices:
        a = iv[:3]
        b = iv[3:6]
        c = iv[6:]
        temp = [x1 + x2 for (x1, x2) in zip(a, c)]
        d = [x1 - x2 for (x1, x2) in zip(temp, b)]
        parallelogram = {'a': a, 'b': b, 'c': c, 'd': d}
        walls.append(parallelogram)
    return walls


def generate_pseudo_measurement_points(para, num_points, noise_max):
    points = []
    # get the normal of the parallelogram
    v1 = [x1 - x2 for (x1, x2) in zip(para['a'], para['b'])]
    v2 = [x1 - x2 for (x1, x2) in zip(para['c'], para['b'])]
    norm = [v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0],
            ]
    length = math.sqrt(norm[0] ** 2 + norm[1] ** 2 + norm[2] ** 2)
    norm = [cor / length for cor in norm]
    norm = [cor * noise_max / 2.0 for cor in norm]
    for i in range(0, num_points):
        p = [random.random(), random.random(), random.random()]
        scaled_a = [cor * p[0] for cor in para['a']]
        scaled_c = [cor * p[1] for cor in para['c']]
        scaled_b = [cor * (1.0 - p[1] - p[0]) for cor in para['b']]
        temp = [x1 + x2 for (x1, x2) in zip(scaled_a, scaled_c)]
        pseudo_point = [x1 + x2 for (x1, x2) in zip(temp, scaled_b)]
        pseudo_point = [c + n * (p[2] - 0.5) for (c, n) in zip(pseudo_point, norm)]
        points.append(pseudo_point)
    return points


def compute_pseudo_dens_grid(points, resolution):
    cube = he.compute_max_cube(points)

    points_np = np.array(points)
    h, edges = np.histogramdd(points_np,
                              [np.arange(cube['x_min'] - 2 * resolution, cube['x_max'] + 2 * resolution, resolution),
                               np.arange(cube['y_min'] - 2 * resolution, cube['y_max'] + 2 * resolution, resolution),
                               np.arange(cube['z_min'] - 2 * resolution, cube['z_max'] + 2 * resolution, resolution)])
    return h, edges


def compute_pseudo_sparse_grid(points, resolution):
    h, edges = compute_pseudo_dens_grid(points, resolution)
    sparse_grid = sp.NDSparseMatrix()
    sparse_grid.from_dense(h)
    return sparse_grid


def main():
    parser = argparse.ArgumentParser(description='Toy example generator for 3D-MDR standard.')
    parser.add_argument('parallelograms_file', type=str,
                        help='File containing list of parallelograms. The file input file format is list of three '
                             'vertices of each of the walls in the environment in a clockwise order')
    parser.add_argument('map_type', type=check_map_type, help='declare map type to save')
    parser.add_argument('output_type', type=check_output_type, help='declare map type to save')

    args = parser.parse_args()

    paras = generate_parallelograms(args.parallelograms_file)
    pseudo_walls = []
    point_cloud = []

    for w in paras:
        points = generate_pseudo_measurement_points(w, 1000, 0.05)
        pseudo_walls.append({'par': w, 'points': points})
        point_cloud.extend(points)

    vis.show_pseudo_measurements(pseudo_walls)

    if args.map_type == 'dense_grid' or args.map_type == 'all':
        h, edges = compute_pseudo_dens_grid(point_cloud, 1)
        if args.output_type == 'plot' or args.output_type == 'all':
            vis.show_pseudo_dense_grid(h)
        if args.output_type == 'json' or args.output_type == 'all':
            jh.save_dense_grid_as_jason(h.shape, h.flatten(), [1, 1, 1])

    # sparse = compute_pseudo_sparse_grid(point_cloud, 1)
    # tree = oc.OctTree(point_cloud, 20)
    # tree.build_tree()
    #
    #
    #
    # vis.show_oct_tree(tree.tree)


if __name__ == "__main__":
    main()
