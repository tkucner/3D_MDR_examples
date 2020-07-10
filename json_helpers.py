import datetime as dt
import json


def save_dense_grid_as_jason(size, voxels, resolution=None, file_name="test_dense_grid", targetpath=""):
    if resolution is None:
        resolution = [1, 1, 1]
    myJSON = {}
    myJSON['localmap_id'] = file_name
    myJSON['time'] = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    myJSON[
        'map_description'] = 'Densegrid local map of ' + file_name
    myJSON['coordinate_system'] = 'relative'
    myJSON['resolution'] = resolution
    myJSON['size'] = size
    myJSON['list_of_characteristics'] = [{'C_name': 'occupancy',
                                          'C_description': '0 if the cell is empty, 1 if the cell is occupied, -1 if the value is unknown',
                                          'C_values': '0 1 -1'}]

    myJSON['list_of_voxels'] = list(voxels)

    with open(targetpath + file_name + '_map.json', 'w') as outfile:
        json.dump(myJSON, outfile)


def save_sparse_grid_as_jason(size, voxels, resolution=None, file_name="test_sparse_grid", targetpath=""):
    if resolution is None:
        resolution = [1, 1, 1]

    myJSON = {}

    myJSON['localmap_id'] = file_name
    myJSON['time'] = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    myJSON[
        'map_description'] = 'Sparse grid local map of ' + file_name
    myJSON['coordinate_system'] = 'relative'
    myJSON['resolution'] = resolution
    myJSON['size'] = size
    myJSON['list_of_characteristics'] = [{'C_name': 'occupancy',
                                          'C_description': '0 if the cell is empty, 1 if the cell is occupied, -1 if the value is unknown',
                                          'C_values': '0 1 -1'}]
    my_voxels = [list(v) for v in voxels]
    myJSON['list_of_voxels'] = my_voxels

    with open(targetpath + file_name + '_map.json', 'w') as outfile:
        json.dump(myJSON, outfile)


def save_point_cloud_as_jason(points, file_name="test_point_cloud", targetpath=""):
    myJSON = {}

    myJSON['localmap_id'] = file_name
    myJSON['time'] = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    myJSON['map_description'] = 'Pointcloud of' + file_name
    myJSON['coordinate_system'] = 'relative'
    myJSON['list_of_characteristics'] = [{'C_name': 'label_id'}]

    myJSON['list_of_points'] = points

    with open(targetpath + file_name + '_map.json', 'w') as outfile:
        json.dump(myJSON, outfile)


def save_oct_map_as_jason(tree, size, file_name="test_oct", targetpath=""):
    myJSON = {}

    myJSON['localmap_id'] = file_name
    myJSON['time'] = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    myJSON[
        'map_description'] = 'Octree local map of ' + file_name
    myJSON['coordinate_system'] = 'relative'

    myJSON['size'] = size
    myJSON['list_of_characteristics'] = [{'C_name': 'occupancy',
                                          'C_description': '0 if the cell is empty, 1 if the cell is occupied, -1 if the value is unknown',
                                          'C_values': '0 1 -1'}]
    temp_tree = []
    for node in tree:
        temp_node = {'node_id': node.oct_id, 'children': node.children}
        temp_tree.append(temp_node)

    myJSON['tree'] = temp_tree
    with open(targetpath + file_name + '_map.json', 'w') as outfile:
        json.dump(myJSON, outfile)


def save_mesh_as_json(mesh, file_name="test_mesh", targetpath=""):
    myJSON = {}

    myJSON['localmap_id'] = file_name
    myJSON['time'] = dt.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    myJSON['map_description'] = 'Polygonmesh local map of ' + file_name
    myJSON['coordinate_system'] = 'relative'
    myJSON['list_of_characteristics_point'] = []
    myJSON['list_of_characteristics_polygon'] = []

    polys = []
    verts_all = []
    for pw in mesh:
        x = [pw['par']['a'][0], pw['par']['b'][0], pw['par']['c'][0], pw['par']['d'][0]]
        y = [pw['par']['a'][1], pw['par']['b'][1], pw['par']['c'][1], pw['par']['d'][1]]
        z = [pw['par']['a'][2], pw['par']['b'][2], pw['par']['c'][2], pw['par']['d'][2]]
        l_vert = list(zip(x, y, z))
        verts_all.extend(l_vert)
        polys.append(l_vert)

    myJSON['list_of_polygons'] = polys
    myJSON['list_of_vertices'] = verts_all

    with open(targetpath + file_name + '_map.json', 'w') as outfile:
        json.dump(myJSON, outfile)
