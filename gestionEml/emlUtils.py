#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


def file_exist(path, error=False):
    _bool = os.path.isfile(path)
    if _bool is False and error is True:
        msg = f"Chemin non trouvé : {path}"
        raise FileNotFoundError(msg)
    return _bool


def define_file_path(directory_path, file_name):
    file_path = os.path.join(
        directory_path, file_name
    )  # config.entry_folder_path, eml_name)
    file_exist(file_path, error=True)
    return file_path
