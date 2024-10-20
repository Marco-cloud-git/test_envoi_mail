#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pathlib import Path


def file_exists(path: str, error=False) -> bool:
    exists = os.path.isfile(path)
    if exists is False and error is True:
        msg = f"Chemin non trouvé : {path}"
        raise FileNotFoundError(msg)
    return exists


def define_file_path(directory_path: str, file_name: str) -> str:
    if directory_path is None or file_name is None:
        msg = f"Les chemins ne peuvent pas être nul, directory_path : {directory_path}, file_name : {file_name}"
        raise ValueError(msg)
    file_path = os.path.join(directory_path, file_name)
    file_path = Path(file_path)
    file_exists(file_path, error=True)
    return file_path


def increment_file_name(file_path: str, increment: int = 1000) -> str:
    directory_name = os.path.dirname(file_path)
    file_name = os.path.basename(file_path)
    base_name, extension = os.path.splitext(file_name)

    exists = file_exists(file_path, error=False)
    if not exists:
        return file_path, file_name
    else:
        for i in range(1, increment + 1):
            new_file_name = f"{base_name}_{i}{extension}"
            new_file_path = os.path.join(directory_name, new_file_name)
            new_file_path = Path(new_file_path)
            exists = file_exists(new_file_path, error=False)
            if not exists:
                return new_file_path, new_file_name

    msg = f"Aucun nom de fichier disponible après {increment} tentatives pour : {file_name}"
    raise ValueError(msg)
