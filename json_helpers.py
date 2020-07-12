import datetime as dt
import json

import helpers as he


def save_dense_grid_as_jason(size, voxels, resolution=None, file_name="test_dense_grid", targetpath=""):
    """
    Function saving the dense grid as a local map into JSON file.
    :param size: three element list representing the size of the map as number of voxels along each dimension
    :param voxels: list of voxels
    :param resolution: three elemnt list describing the size of a voxel a long each dimension
    :param file_name: name of the file to be saved as
    :param targetpath: directory where the map will be saved
    """
    if resolution is None:
        resolution = [1, 1, 1]
    myJSON = {'localmap_id': file_name, 'time': dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
              'map_description': 'Densegrid local map of ' + file_name, 'coordinate_system': 'relative',
              'resolution': resolution, 'size': size, 'list_of_characteristics': [{'C_name': 'occupancy',
                                                                                   'C_description': '0 if the cell is empty, 1 if the cell is occupied, -1 if the value is unknown',
                                                                                   'C_values': '0 1 -1'}],
              'list_of_voxels': list(voxels)}

    with open(targetpath + file_name + '_map.json', 'w') as outfile:
        json.dump(myJSON, outfile)


def save_sparse_grid_as_jason(size, voxels, resolution=None, file_name="test_sparse_grid", targetpath=""):
    """
    Function saving the sparse grid as a local map into JSON file.
    :param size: three element list representing the size of the map in meters
    :param voxels: list of sparse voxels
    :param resolution: three elemnt list describing the size of a voxel a long each dimension
    :param file_name: name of the file to be saved as
    :param targetpath: directory where the map will be saved

    """
    if resolution is None:
        resolution = [1, 1, 1]

    myJSON = {'localmap_id': file_name, 'time': dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
              'map_description': 'Sparse grid local map of ' + file_name, 'coordinate_system': 'relative',
              'resolution': resolution, 'size': size, 'list_of_characteristics': [{'C_name': 'occupancy',
                                                                                   'C_description': '0 if the cell is empty, 1 if the cell is occupied, -1 if the value is unknown',
                                                                                   'C_values': '0 1 -1'}]}

    my_voxels = [list(v) for v in voxels]
    myJSON['list_of_voxels'] = my_voxels

    with open(targetpath + file_name + '_map.json', 'w') as outfile:
        json.dump(myJSON, outfile)


def save_point_cloud_as_jason(points, file_name="test_point_cloud", targetpath=""):
    """
    Function saving the sparse grid as a local map into JSON file.
    :param points: List of point coordiantes to be saved
    :param file_name: name of the file to be saved as
    :param targetpath: directory where the map will be saved
    """
    myJSON = {'localmap_id': file_name, 'time': dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
              'map_description': 'Pointcloud of' + file_name, 'coordinate_system': 'relative',
              'list_of_characteristics': [{'C_name': 'label_id'}], 'list_of_points': points}

    with open(targetpath + file_name + '_map.json', 'w') as outfile:
        json.dump(myJSON, outfile)


def save_oct_map_as_jason(tree, size, file_name="test_oct", targetpath=""):
    """
    Function saving the oct-map as a local map into JSON file.
    :param tree: the oct tree represneted as a list of nodes
    :param size: The size of the map dented in meters
    :param file_name: name of the file to be saved as
    :param targetpath: directory where the map will be saved
    """
    myJSON = {'localmap_id': file_name, 'time': dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
              'map_description': 'Octree local map of ' + file_name, 'coordinate_system': 'relative', 'size': size,
              'list_of_characteristics': [{'C_name': 'occupancy',
                                           'C_description': '0 if the cell is empty, 1 if the cell is occupied, -1 if the value is unknown',
                                           'C_values': '0 1 -1'}]}

    temp_tree = []
    for node in tree:
        temp_node = {'node_id': node.oct_id, 'children': node.children}
        temp_tree.append(temp_node)

    myJSON['tree'] = temp_tree
    with open(targetpath + file_name + '_map.json', 'w') as outfile:
        json.dump(myJSON, outfile)


def save_mesh_as_json(mesh, file_name="test_mesh", targetpath=""):
    """
    Function saving the mesh as a local map into JSON file.
    :param mesh: The input list of polygons building map.
    :param file_name: name of the file to be saved as
    :param targetpath: directory where the map will be saved
    """
    myJSON = {'localmap_id': file_name, 'time': dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
              'map_description': 'Polygonmesh local map of ' + file_name, 'coordinate_system': 'relative',
              'list_of_characteristics_point': [], 'list_of_characteristics_polygon': []}

    polys = []
    verts_all = []
    for pw in mesh:
        x, y, z = he.get_points_from_mesh(pw)
        l_vert = list(zip(x, y, z))
        verts_all.extend(l_vert)
        polys.append(l_vert)

    myJSON['list_of_polygons'] = polys
    myJSON['list_of_vertices'] = verts_all

    with open(targetpath + file_name + '_map.json', 'w') as outfile:
        json.dump(myJSON, outfile)
