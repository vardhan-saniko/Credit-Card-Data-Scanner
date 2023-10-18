import os
import json

current_file_path = os.path.abspath(__file__)
parent_directory = os.path.dirname(current_file_path)
config_file_path = os.path.join(parent_directory, 'config.json')

print(config_file_path)

with open(config_file_path, 'r') as file:
    json_data = file.read()

json_dict = json.loads(json_data)


class Config:
    def __init__(self):
        for key, val in json_dict.items():
            setattr(self, '%s' % (key,), val)
