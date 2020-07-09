import datetime as dt
import json


def save_dense_grid_as_jason(size, voxels, resolution=None, file_name="test_map_dense_grid", targetpath=""):
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
    print(myJSON)

    with open(targetpath + file_name + '_map.json', 'w') as outfile:
        json.dump(myJSON, outfile)
