#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from time import perf_counter
import depotEml.config as config
from gestionEml.eml import Eml, ModifyEml, execute_eml_modification, modify, define_file_path
import imap.connexionIMAP as connexionIMAP

############### Parametrages IMAP ###############
#"outlook.office365.com"
imap_serveur = (
    "imap-mail.outlook.com"
)
port_imap = 993
email_adress = "jeandelaged@outlook.fr"
password = ""


############### Gestion Eml ###############
eml_name_1 = "2331459201382 nom PJ trop long.eml"
eml_name_2 = "eml avec 2 docs PDF dont 1 multipages.eml"
eml_name_3 = "eml avec 3 PJ portant le meme nom.eml"
eml_name_4 = "piece jointe docx.eml"
eml_name_5 = "PJ PDF qui contient une couche texte.eml"
eml_name_6 = "PJ zip contenant 2 docs du meme nom.eml"
eml_name_7 = "test YAHOO PJ nom avec caractères spéciaux.eml"
list_eml = [eml_name_1, eml_name_2, eml_name_3,
            eml_name_4, eml_name_5, eml_name_6, eml_name_7]

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


# on s'en fout pour le moment
def main(process, file_name):
    entry_folder_path, destination_folder_path = config.config_controle_directory(
        config.dict_directory
    )
    execute_eml_modification(
        process, file_name, entry_folder_path, destination_folder_path)


def connect_imap(file_name):
    # se connecter
    imap = connexionIMAP.connexion(
        imap_serveur, port_imap, email_adress, password)

    # avoir la liste des dossier de la boite mail
    mailBoxlist = connexionIMAP.listerDossier(imap)

    # afficher la liste des dossiers
    print(f"Liste des dossiers de la boite mail : {mailBoxlist}")

    # compter le nombre de mail dans la messagerie
    connexionIMAP.count_mail_from_mailbox(imap, mailBoxlist)

    # faire des listes d'identifiant de mail par dossier
    dossier_a_lire = "INBOX"  # "Brouillons"   #"INBOX"
    # liste des uuid
    print(connexionIMAP.listerUidMail(imap, dossier_a_lire))
    # afficher une liste de mail dans un dossier
    # print(connexionIMAP.listerMail(imap, dossier_a_lire))

    # lire l'en tête d'un eml et afficher eventuellement le message pour un eml à une postion precise dans un dossier donne
    # 1)  # 1, "Oui") #1, "Non")
    # connexionIMAP.lireMail(imap, dossier_a_lire, 1, "Oui")

    # se deconnecter
    connexionIMAP.deconnexion(imap)


################## Fonctions pour la demonstration ##################
def exemple_1(eml_file_path, destination_folder_path):
    # exemple 1 : avec toutes les fonctions disponibles
    # Charger l'email d'entrée
    eml = Eml(eml_file_path)
    # autres fonctionnalités : afficher touts les paramétres et exemple d'un get pour obtenir le nom
    # Eml.print_eml_data(eml, eml_data=False)
    file_name = eml.get_name()

    # # Construire le chemin de destination
    destination_file_path = os.path.join(destination_folder_path, file_name)

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

    # sauvegarder
    eml_modifier.save(destination_file_path)

    date = eml.get_date()
    message_id = eml.get_message_id()

    return date, message_id


def exemple_2(eml_file_path, destination_folder_path):
    # exemple 2 : avec seulement la fonction set
    date, message_id = modify(
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
    return date, message_id


################## Pour lancer le script ##################
if __name__ == "__main__":
    ############### lancement par main ###############
    # main(process=exemple_1, file_name=list_eml)

    ############### ce que l'on aurait en roboframework ###############
    file_name = "2331459201382 nom PJ trop long.eml"
    list_file_name = list_eml

    entry_folder_path, destination_folder_path = config.config_controle_directory(
        config.dict_directory)

    ########## proposition 1 : avec wrapper ##########

    ##### cas exemple_1 pour 1 eml #####
    list_eml_data = execute_eml_modification(process=exemple_1, file_name=file_name,
                                          entry_folder_path=entry_folder_path, destination_folder_path=destination_folder_path)
    print(list_eml_data)

    ##### cas exemple_1 pour une liste d'eml #####
    # list_eml_data = execute_eml_modification(process=exemple_1, file_name=list_file_name,
    #                                       entry_folder_path=entry_folder_path, destination_folder_path=destination_folder_path)
    # print(list_eml_data)

    ##### cas exemple_2 pour 1 eml #####
    # list_eml_data = execute_eml_modification(process=exemple_2, file_name=file_name,
    #                                       entry_folder_path=entry_folder_path, destination_folder_path=destination_folder_path)
    # print(list_eml_data)

    ##### cas exemple_2 pour une liste d'eml #####
    # list_eml_data = execute_eml_modification(process=exemple_2, file_name=list_file_name,
    #                                       entry_folder_path=entry_folder_path, destination_folder_path=destination_folder_path)
    # print(list_eml_data)

    ########## proposition 2 : sans wrapper -> ne gére pas les listes ##########
    # file_path = define_file_path(
    #         directory_path=entry_folder_path, file_name=file_name
    #     )

    ##### cas exemple_3 #####
    # date, message_id = modify(
    #     file_path=file_path,
    #     destination_folder=destination_folder_path,
    #     subject=new_subject,
    #     sender=new_sender,
    #     return_path=new_return_path,
    #     reply_to=new_reply_to,
    #     to=new_to,
    #     cc=new_cc,
    #     bcc=new_cc,
    # )
    # print(f"date : {date}, message_id : {message_id}")
    ##### cas exemple_4 #####
    # eml = Eml(file_path)
    # destination_file_path = os.path.join(destination_folder_path, file_name)
    # eml_modifier = ModifyEml(eml)
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
    # date = eml.get_date()
    # message_id = eml.get_message_id()
    # print(f"date : {date}, message_id : {message_id}")
