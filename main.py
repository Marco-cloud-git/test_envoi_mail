#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from eml import Eml, ModifyEml
import utils
import os
import config

eml_name = "test YAHOO PJ nom avec caractères spéciaux.eml"
eml_file_path = os.path.join(config.entry_folder_path, eml_name)

new_subject = "Super toto"  # None
new_sender = "new_sender@test.fr"
new_reply_to = None  # "new_reply_to@test.fr"
new_return_path = "new_return_path@test.fr"
new_to = "my_to@test.fr", "2x_to@test.fr"
new_cc = None       #"my_cc@test.fr"
new_bcc = None


def main(eml_file_pat):
    # Vérifier que le répertoire de sortie existe
    utils.directory_exist(config.entry_folder_path)
    utils.directory_exist(config.destination_folder_path)

    # Vérifier que le fichier existe
    utils.file_exist(eml_file_path)

    # Charger l'email d'entrée
    eml = Eml(eml_file_pat)
    Eml.print_eml_data(eml, eml_data=False)
    name = eml.get_name()
    # # Construire le chemin de destination et sauvegarder
    destination_file_path = os.path.join(config.destination_folder_path, name)
    # print(f"Destination : {destination_file_path}")

    # Créer un modificateur pour l'objet Eml
    eml_modifier = ModifyEml(eml)
    # # Modifier la date, l'expéditeur, Return_Path et Reply_To
    eml_modifier.modify(
        subject=new_subject, sender=new_sender, reply_to=new_reply_to, return_path=new_return_path, cc=new_cc, bcc=new_bcc
    )
    eml_modifier.add_recipient(recipient=new_to, field_name="To")
    eml_modifier.add_recipient(recipient=new_cc, field_name="Cc")
    # # Sauvegarder l'email modifié
    eml_modifier.save(destination_file_path)


if __name__ == "__main__":
    file_path = "entree_eml/test YAHOO PJ nom avec caractères spéciaux.eml"
    main(file_path)
