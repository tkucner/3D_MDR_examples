#Simple MDR-3D toy example generator
## Introduction
This repository is part of IEEE AS WG for developing standard for exchanging 3D maps.
## How to use it
This software generates a simulated measurements a long polygons, which represent virtual walls.

To obtain a toy example prepare a csv file, where each row describe a parallelogram simulating a wall in the environment.
Each row should const out of 9 numbers denoting three vertices of the parallelogram in clockwise or counter-clockwise order.:
```
x_1, y_1, z_1, x_2, y_2, z_2, x_3, y_3, z_3
```
Then run the code as:
```
$ python toy_example_generator input_file [map_type] [output_type]
```
There are four types of maps the system can generate:
* `dense_grid` dense grid
* `sparse_grid` sparse grid
* `oct_map` octomap
* `mesh` mesh
* `pc` point cloud
* `all` converst map to all possible formats

The map can be eitheer saved to a JSON file `json`, visualised `plot` or both `all`.



