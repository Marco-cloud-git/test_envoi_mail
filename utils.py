#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


def file_exist(path, error=False):
    _bool = os.path.isfile(path)
    if _bool is False and error is True:
        msg = f"Le fichier n'est pas trouvé : {path}"
        raise FileNotFoundError(msg)
    return _bool


def directory_exist(path):
    if not os.path.isdir(path):
        msg = f"Le dossier n'est pas trouvé : {path}"
        raise FileNotFoundError(msg)


def controle_directory(dict_directory):
    # Vérifier que le répertoire de sortie existe
    for name, path in dict_directory.items():
        directory_exist(path)


def define_file_path(directory_path, file_name):
    file_path = os.path.join(
        directory_path, file_name
    )  # config.entry_folder_path, eml_name)
    file_exist(file_path, error=True)
    return file_path
