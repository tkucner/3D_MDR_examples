import os, json
import fastjsonschema

schema_file_path = 'Json_schema/local_maps_JSON/sparsegrid.json'
json_folder_path = 'Converter/Densegrid Sparsegrid Octomap - Uni_Freiburg/sparsegrid_json/'

with open(schema_file_path, 'r') as f:
    my_schema = json.load(f)
    
validator = fastjsonschema.compile(my_schema)

def validate_json(filename):
    print(filename + ":   ", end="", flush=True)
    with open(json_folder_path + filename, "r") as f:
        my_json = json.load(f)
    validator(my_json)
    print("OK")

for file in os.listdir(json_folder_path):
    print('*************************************************************************************')
    validate_json(file)
