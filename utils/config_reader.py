import json

def read_json_config(file_path):
    with open(file_path) as f:
        return json.load(f)