#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os


def directory_exist(path):
    if path is None or not os.path.isdir(path):
        msg = f"Le dossier n'est pas trouvé : {path}"
        raise FileNotFoundError(msg)


def controle_directory(dict_directory):
    # Vérifier que le répertoire de sortie existe
    for name, path in dict_directory.items():
        directory_exist(path)
