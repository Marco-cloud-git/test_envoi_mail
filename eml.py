#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email import policy
from email.parser import BytesParser
import os
from text_encoding import TextEncoding


class Eml:
    def __init__(self, file_path):
        self.file_path = file_path
        self.eml_data = self.load_eml(file_path)
        self.get_metadata()

    def load_eml(self, file_path):
        with open(file_path, "rb") as f:
            return BytesParser(policy=policy.default).parse(f)

    def get_metadata(self):
        self.name = self.get_name()
        self.sender = self.get_sender()
        self.to = self.get_to()
        self.cc = self.get_cc()
        self.bcc = self.get_bcc()
        self.reply_to = self.get_reply_to()
        self.return_path = self.get_return_path()
        self.date = self.get_date()
        self.message_id = self.get_message_id()
        self.subject = self.get_subject()
        # self.body = self.get_body()

    def print_eml(self):
        print("Name:", self.name)
        print("Sender:", self.sender)
        print("To:", self.to)
        print("Cc:", self.cc)
        print("Bcc:", self.bcc)
        print("Reply-To:", self.reply_to)
        print("Return-Path:", self.return_path)
        print("Date:", self.date)
        print("Message-ID:", self.message_id)
        print("Subject:", self.subject)

    def get_name(self):
        return os.path.basename(self.file_path)

    def get_sender(self):
        return TextEncoding.decode_header(self.eml_data["From"])

    def get_to(self):
        return self._get_addresses("To")

    def get_cc(self):
        return self._get_addresses("Cc")

    def get_bcc(self):
        return self._get_addresses("Bcc")

    def get_reply_to(self):
        return TextEncoding.decode_header(self.eml_data["Reply-To"])

    def get_return_path(self):
        return TextEncoding.decode_header(self.eml_data["Return-Path"])

    def get_date(self):
        return self.eml_data["Date"]

    def get_message_id(self):
        return self.eml_data["Message-ID"]

    def get_subject(self):
        return self.eml_data["Subject"]

    def get_body(self):
        try:
            if self.eml_data.is_multipart():
                return "".join(
                    part.get_content()
                    for part in self.eml_data.iter_parts()
                    if part.get_content_type() == "text/plain"
                )
            else:
                return self.eml_data.get_body(preferencelist=("plain")).get_content()
        except Exception as e:
            print("Error retrieving body:", e)
            return None

    def _get_addresses(self, field_name):
        """
        Helper method to parse multiple email addresses in the To, Cc, and Bcc fields.
        """
        addresses = self.eml_data[field_name]
        if addresses:
            return [TextEncoding.decode_header(addr) for addr in addresses.split(",")]
        return []

    def as_bytes(self):
        return self.eml_data.as_bytes()


class ModifyEml:
    def __init__(self, eml_object):
        """
        Initialise l'objet avec un email Eml existant.
        """
        if eml_object is None:
            raise ValueError("L'objet EML fourni est None.")
        else:
            self._object = eml_object  # Composition : `ModifyEml` contient `Eml`

    def set_sender(self, sender, return_path=None, reply_to=None):
        """
        Modifie les adresses de l'expediteur, du reply-to et du return_path de l'email.
        :param sender: Nouvelle adresse email de l'expéditeur (string).
        """
        self.set_mail_sender(sender)
        if return_path is not None:
            self.set_return_path(return_path)
        if reply_to is not None:
            self.set_reply_to(reply_to)

    def set_mail_sender(self, mail_sender):
        """
        Modifie l'expéditeur de l'email.
        :param mail_sender: Nouvelle adresse email de l'expéditeur (string).
        """
        self._object.eml_data.replace_header("From", mail_sender)

    def set_return_path(self, return_path):
        """
        Modifie les adresses de retour de l'email.
        :param new_reply_to: Nouvelle adresse email de réponse du mail (string).
        :param new_return_path: Nouvelle adresse email de retour du mail en cas d'erreur (string).
        """
        if self._object.return_path is not None and self._object.return_path != "":
            self._object.eml_data.replace_header("Return-Path", return_path)

    def set_reply_to(self, reply_to):
        """
        Modifie les adresses de retour de l'email.
        :param new_reply_to: Nouvelle adresse email de réponse du mail (string).
        :param new_return_path: Nouvelle adresse email de retour du mail en cas d'erreur (string).
        """
        if self._object.reply_to is not None and self._object.reply_to != "":
            self._object.eml_data.replace_header("Reply-To", reply_to)

    # def add_recipient(self, recipient, field_name='To'):
    #     """
    #     Ajoute un destinataire à un champ spécifique (To, Cc, ou Bcc).
    #     :param recipient: Adresse email du destinataire (string).
    #     :param field_name: Champ de destinataire (par défaut 'To').
    #     """
    #     if field_name not in ['To', 'Cc', 'Bcc']:
    #         raise ValueError("Le champ de destinataire doit être 'To', 'Cc', ou 'Bcc'")

    #     # Récupérer l'adresse existante et ajouter le destinataire si nécessaire
    #     current_recipients = self.eml.eml_object[field_name]
    #     if current_recipients:
    #         new_recipients = f"{current_recipients}, {recipient}"
    #     else:
    #         new_recipients = recipient

    #     self.eml.eml_object.replace_header(field_name, new_recipients)

    # def set_recipients(self, recipients, field_name='To'):
    #     """
    #     Remplace les destinataires d'un champ spécifique (To, Cc, ou Bcc).
    #     :param recipients: Liste d'adresses email (list de strings).
    #     :param field_name: Champ de destinataire à modifier (par défaut 'To').
    #     """
    #     if field_name not in ['To', 'Cc', 'Bcc']:
    #         raise ValueError("Le champ de destinataire doit être 'To', 'Cc', ou 'Bcc'")

    #     # Joindre les nouvelles adresses email
    #     new_recipients = ', '.join(recipients)
    #     self.eml.eml_object.replace_header(field_name, new_recipients)

    # def remove_recipient(self, recipient, field_name='To'):
    #     """
    #     Supprime un destinataire spécifique d'un champ (To, Cc, ou Bcc).
    #     :param recipient: Adresse email du destinataire à supprimer (string).
    #     :param field_name: Champ de destinataire où chercher l'adresse (par défaut 'To').
    #     """
    #     if field_name not in ['To', 'Cc', 'Bcc']:
    #         raise ValueError("Le champ de destinataire doit être 'To', 'Cc', ou 'Bcc'")

    #     current_recipients = self.eml.eml_object[field_name]
    #     if current_recipients:
    #         # Retirer le destinataire et réenregistrer les adresses
    #         updated_recipients = ', '.join(
    #             addr.strip() for addr in current_recipients.split(',') if addr.strip() != recipient
    #         )
    #         self.eml.eml_object.replace_header(field_name, updated_recipients)

    # def remove_all_recipient(self, recipient):
    #     fields=['To', 'Cc', 'Bcc']
    #     for field_name in fields:
    #         self.remove_recipient(self, recipient, field_name)

    # def get_email_message(self):
    #     """
    #     Retourne l'objet email avec les modifications appliquées.
    #     """
    #     return self.eml.eml_object

    def save(self, new_file_path):  # =None):
        if not hasattr(self._object, "as_bytes"):
            raise AttributeError("L'objet EML ne possède pas de méthode 'as_bytes'.")
        with open(new_file_path, "wb") as f:
            f.write(self._object.as_bytes())
