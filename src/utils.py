import json
import os

def read_json(filepath):
    '''Function to read data from a json file.'''
    with open(filepath,'r+') as f:
        data = json.load(f)
    return data

def save_to_json(data, filepath):
    '''Function to save data to json file.'''
    if not os.path.isfile(filepath):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath,'w') as f:
            json.dump(data, f)
    return data
    