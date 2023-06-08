"""This module is about handling files"""

import json
import os


def list_of_objects_to_json(list_of_objects: list, file_path: str):
    """Write a list of objects to a json file"""
    objects_list = []
    for object in list_of_objects:
        object_dict = object.__dict__
        objects_list.append(object_dict)
    with open(file_path, "w") as file:
        json.dump(objects_list, file, indent=4)
    print(f"Datas successfully saved to {file_path}")


def add_same_type_object_to_json(object, file_path: str):
    object_dict = object.__dict__
    if os.path.exists(file_path):
        with open(file_path, "a") as file:
            json.dump(object_dict, file, indent=4)
        print(f"{object} successfully added to {file_path}")
    else:
        print(f"Error: {file_path} not found")
        return None


def json_to_dict(file_path: str):
    """Convert a json file into a dictionary"""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            datas_dict = json.load(file)
        return datas_dict
    else:
        print(f"Error: {file_path} not found")
        return None
