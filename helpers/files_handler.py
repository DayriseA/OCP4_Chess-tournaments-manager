"""This module is about handling files"""

import json
import os, shutil


def list_of_objects_to_json(list_of_objects: list, file_path: str):
    """Write a list of objects to a json file"""
    objects_list = []
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
    for each_object in list_of_objects:
        object_dict = each_object.__dict__
        objects_list.append(object_dict)
    with open(file_path, "w") as file:
        json.dump(objects_list, file, indent=4)
    print(f"{file_path} successfully saved")


def json_to_dict(file_path: str):
    """Convert a json file into a dictionary"""
    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            datas_dict = json.load(file)
        return datas_dict
    else:
        print(f"{file_path} not found, normal if running the app for 1st time")
        return None


def copy_rename_file(file_path: str, copy_file_path: str):
    """Copy and rename a file"""
    if os.path.exists(file_path):
        shutil.copy(file_path, copy_file_path)
