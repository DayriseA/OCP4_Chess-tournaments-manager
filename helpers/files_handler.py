"""This module is about handling files"""

import json
import os, shutil


def list_of_objects_to_json(list_of_objects: list, file_path: str):
    """Write a list of objects to a json file"""
    objects_list = []
    for each_object in list_of_objects:
        object_dict = each_object.__dict__
        objects_list.append(object_dict)
    if os.path.exists(file_path):
        with open(file_path, "w") as file:
            json.dump(objects_list, file, indent=4)
        print(f"{file_path} successfully saved")
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


def copy_rename_file(file_path: str, copy_file_path: str):
    """Copy and rename a file"""
    if os.path.exists(file_path):
        shutil.copy(file_path, copy_file_path)
    else:
        print(f"Error: {file_path} not found")
        return None
