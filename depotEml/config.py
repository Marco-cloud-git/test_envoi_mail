#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# from pathlib import Path
from functools import wraps
from depotEml.configUtils import controle_directory

# Chemins des dossiers
entry_folder_path = "depotEml/entree"
destination_folder_path = "depotEml/sortie"

dict_directory = {
    "entry_folder_path": entry_folder_path,
    "destination_folder_path": destination_folder_path,
}


# Définition du wrapper pour la fonction controle_directory
def wrapper_controle_directory(func):
    @wraps(func)
    def wrapper(dict_directory):
        # Appeler la fonction d'origine pour vérifier les répertoires
        func(dict_directory)

        # Extraire les chemins
        entry_folder_path = dict_directory.get("entry_folder_path")
        # entry_folder_path = Path(entry_folder_path)
        destination_folder_path = dict_directory.get("destination_folder_path")
        # destination_folder_path = Path(destination_folder_path)

        if entry_folder_path is None or destination_folder_path is None:
            raise ValueError(
                "Erreur : Les chemins d'entrée ou de destination ne sont pas valides."
            )

        return entry_folder_path, destination_folder_path

    return wrapper


# Appliquer le wrapper à la fonction controle_directory
config_controle_directory = wrapper_controle_directory(controle_directory)
