#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

def file_exist(path):
    if not os.path.isfile(path):
        msg=f"Le fichier n'est pas trouvé : {path}"
        raise FileNotFoundError(msg)

def directory_exist(path):
    if not os.path.isdir(path):
        msg=(f"Le dossier n'est pas trouvé : {path}")
        raise FileNotFoundError(msg)
