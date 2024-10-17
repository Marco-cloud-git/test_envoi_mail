#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from eml import Eml, ModifyEml
import utils
import os
import config

eml_name = "test YAHOO PJ nom avec caractères spéciaux.eml"
eml_file_path = os.path.join(config.entry_folder_path, eml_name)

new_subject = "New subject"  # None
new_sender = "new_sender@test.fr"
new_reply_to = "new_reply_to@test.fr"
new_return_path = "new_return_path@test.fr"
new_to = "new_to@test.fr", "2x_to@test.fr"
new_cc = "new_cc@test.fr", "2x_cc@test.fr", "3x_cc@test.fr"
another_cc = "4x_cc@test.fr"
and_another_cc = None
cc_to_remove = "3x_cc@test.fr"
another_cc_to_remove = None
new_bcc = "new_bcc@test.fr"
remove_cc_adress = '"adresse_secondaire@test" <adresse_secondaire@test>'


def main(eml_file_pat):
    # Vérifier que le répertoire de sortie existe
    utils.directory_exist(config.entry_folder_path)
    utils.directory_exist(config.destination_folder_path)

    # Vérifier que le fichier existe
    utils.file_exist(eml_file_path)

    # Charger l'email d'entrée
    eml = Eml(eml_file_pat)
    # Eml.print_eml_data(eml, eml_data=False)
    name = eml.get_name()
    # # Construire le chemin de destination et sauvegarder
    destination_file_path = os.path.join(config.destination_folder_path, name)

    # Créer l'objet à modifier
    eml_modifier = ModifyEml(eml)
    # modifier les valeurs
    eml_modifier.set_message_id()
    eml_modifier.set_subject(new_subject)
    eml_modifier.set_from(new_sender)
    eml_modifier.set_return_path(new_return_path)
    eml_modifier.set_reply_to(new_reply_to)
    eml_modifier.set_cc(new_cc)
    eml_modifier.set_cc(another_cc)
    eml_modifier.set_bcc(new_bcc)
    eml_modifier.add_to(new_to)
    eml_modifier.add_cc(new_cc)
    eml_modifier.add_cc(cc_to_remove)
    eml_modifier.add_cc(another_cc)
    eml_modifier.add_cc(and_another_cc)
    eml_modifier.remove_cc(cc_to_remove)
    eml_modifier.remove_cc(another_cc_to_remove)
    eml_modifier.add_bcc(recipient=new_bcc)

    eml_modifier.save(destination_file_path)


if __name__ == "__main__":
    file_path = "entree_eml/test YAHOO PJ nom avec caractères spéciaux.eml"
    main(file_path)
