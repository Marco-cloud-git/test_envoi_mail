#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from eml import Eml, ModifyEml, modify
import utils
import os
import config

eml_name = "test YAHOO PJ nom avec caractères spéciaux.eml"


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


def main(file_name):
    entry_folder_path, destination_folder_path = config.config_controle_directory(
        config.dict_directory
    )

    # Vérifier que le fichier existe
    eml_file_path = utils.define_file_path(
        directory_path=entry_folder_path, file_name=file_name
    )


### exemple 1 : avec toutes les fonctions disponibles
    # # Charger l'email d'entrée
    # eml = Eml(eml_file_path)
    # ### autres fonctionnalités
    # ## Eml.print_eml_data(eml, eml_data=False)
    # ##name = eml.get_name()

    # # # Construire le chemin de destination et sauvegarder
    # destination_file_path = os.path.join(destination_folder_path, file_name)

    # # Créer l'objet à modifier
    # eml_modifier = ModifyEml(eml)
    # # modifier les valeurs
    # eml_modifier.set_message_id()
    # eml_modifier.set_subject(new_subject)
    # eml_modifier.set_from(new_sender)
    # eml_modifier.set_return_path(new_return_path)
    # eml_modifier.set_reply_to(new_reply_to)
    # eml_modifier.set_cc(new_cc)
    # eml_modifier.set_cc(another_cc)
    # eml_modifier.set_bcc(new_bcc)
    # eml_modifier.add_to(new_to)
    # eml_modifier.add_cc(new_cc)
    # eml_modifier.add_cc(cc_to_remove)
    # eml_modifier.add_cc(another_cc)
    # eml_modifier.add_cc(and_another_cc)
    # eml_modifier.remove_cc(cc_to_remove)
    # eml_modifier.remove_cc(another_cc_to_remove)
    # eml_modifier.add_bcc(recipient=new_bcc)

    # eml_modifier.save(destination_file_path)

### exemple 2 : avec seulement la fonction set
    modify(
        file_path=eml_file_path,
        destination_folder=destination_folder_path,
        subject=new_subject,
        sender=new_sender,
        return_path=new_return_path,
        reply_to=new_reply_to,
        to=new_to,
        cc=new_cc,
        bcc=new_cc,
    )


if __name__ == "__main__":
    main(file_name=eml_name)
