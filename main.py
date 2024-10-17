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
new_cc = "my_cc@test.fr"
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
    # eml_modifier.set_subject(new_subject)
    # eml_modifier.set_sender(new_sender)
    # eml_modifier.set_return_path(new_return_path)
    # eml_modifier.set_reply_to(new_reply_to)
    eml_modifier.set_recipient(recipient=new_cc, field_name="Cc")
    eml_modifier.add_recipient(recipient=new_to, field_name="To")
    # eml_modifier.add_recipient(recipient=new_bcc, field_name="Bcc", )

    eml_modifier.save(destination_file_path)
    # for value in eml_modifier.eml_object.__dict__:
    #     print(f"{value} : {getattr(eml_modifier.eml_object, value)}")

    # eml_modifier.remove_recipient_from_field(
    #     recipient=remove_cc_adress, field_name="Cc"
    # )
    # # Sauvegarder l'email modifié
    # eml_modifier.save(destination_file_path)


if __name__ == "__main__":
    file_path = "entree_eml/test YAHOO PJ nom avec caractères spéciaux.eml"
    main(file_path)
