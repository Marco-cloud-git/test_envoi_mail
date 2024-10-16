#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email import policy
from email.parser import BytesParser
from email.utils import format_datetime, make_msgid
import os
from text_encoding import TextEncoding
from datetime import datetime
import pytz
from functools import wraps


class Eml:
    def __init__(self, file_path):
        self.file_path = file_path
        self.eml_data = self.load_eml(file_path)
        self.get_data()

    def load_eml(self, file_path):
        with open(file_path, "rb") as f:
            return BytesParser(policy=policy.default).parse(f)

    def get_data(self):
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

    def print_eml_data(self, eml_data=False):
        """
        Affiche les valeurs des paramétres de l'instances.
        :param eml_data: par defaut: False, le texte de l'eml n'est pas affiché.
        """
        for item in self.__dict__:
            if item.startswith('_'):
                continue  # Ignore les attributs privés

            if eml_data is True:
                self._show_attribute(item)
            else:
                if item != "eml_data":
                    self._show_attribute(item)

    def _show_attribute(self, item):
        value = getattr(self, item, None)
        print(item, value)

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
            self.eml_object = eml_object  # Composition : `ModifyEml` contient `Eml`

    # decorateur pour modifier les adresses mails de destination à partir d'une liste.
    def with_recipient_list(func):
        @wraps(func)
        def wrapper(self, recipient, *args, **kwargs):
            # Si email est une liste, on appelle func pour chaque adresse
            if isinstance(recipient, list) or isinstance(recipient, tuple):
                for address in recipient:
                    func(self, address, *args, **kwargs)
            else:
                # Si email n'est pas une liste, on l'appelle une seule fois
                func(self, recipient, *args, **kwargs)

        return wrapper

    def value_exist_in_field(self, field):
        """
        Test si le champs existe et contient une valeur.
        Evite de rechercher dans le texte du mail si le champs existe.
        :param field: le champs à tester (string).
        :param value: nouvelle valeur de la balise.
        """
        _bool = False
        if field is not None:
            field = ModifyEml.convert_field_name(field)
            field_value = getattr(self.eml_object, field)
            if field_value is not None and len(field_value) > 0:
                _bool = True
        return _bool

    def convert_field_name(field):
        if field in ["To", "Cc", "Bcc", "From", "Return-Path", "Reply-To", "Date", "Subject", "Message-ID"]:
            switch = {
                "To": "to",
                "Cc": "cc",
                "Bcc": "bcc",
                "From": "sender",
                "Return-Path": "return_path",
                "Reply-To": "reply_to",
                "Date": "date",
                "Subject": "subject",
                "Message-ID": "message_id"
            }
            return switch.get(field, 'Not a field')
        else:
            field

    def set_item(self, item, value):
        """
        Modifie la valeur d'une balise dans le header de l'email.
        :param item: nom de la balise à modifier (string).
        :param value: nouvelle valeur de la balise.
        """
        # if self.eml_object.eml_data[item] is not None and value is not None:
        #     self.eml_object.eml_data.replace_header(item, value)
        if self.value_exist_in_field(item) is True and value is not None:
            self.eml_object.eml_data.replace_header(item, value)

    def list_adresse_from_string(adress):
        """
        Permet de découper la chaine de caractère contenant les adresses mails.
        Retourne une liste d'adresses.
        :param recipient: une ou plusieurs adresses mails
        """
        list_adress = list(map(str.strip, adress.split(",")))
        return list_adress

    def modify(
        self, subject=None, sender=None, return_path=None, reply_to=None, to=None, cc=None, bcc=None
    ):
        """
        Modifie le sujet, les adresses de l'expediteur, du reply-to, du return_path de l'email, du destinataire principale, du destinataire secondaire, du destinataire caché, de la date et du message_id.
        :param subjetc: Nouvelle sujet du mail (string).
        :param sender: Nouvelle adresse email de l'expéditeur (string).
        :param return_path: Nouvelle adresse email de réponse en cas d'erreur (string).
        :param reply_to: Nouvelle adresse email pour la réponse (string).
        :param to: Nouveau destinataire principale (string).
        :param cc: Nouveau destinataire secondaire  (string).
        :param bcc: Nouveau destinataire caché  (string).
        """
        # value = getattr(self, item, None)
        # print(self.__dict__)

        self.set_date(timezone_str="Europe/Paris")
        self.set_message_id()
        self.set_subject(subject)
        self.set_sender(sender)
        self.set_return_path(return_path)
        self.set_reply_to(reply_to)

    def set_subject(self, subject):
        """
        Modifie le sujet de l'email.
        :param subject: Nouveau sujet de l'email.
        """
        self.set_item("Subject", subject)

    def set_sender(self, mail_sender):
        """
        Modifie l'expéditeur de l'email.
        :param mail_sender: Nouvelle adresse email de l'expéditeur (string).
        """
        self.set_item("From", mail_sender)

    def set_return_path(self, return_path):
        """
        Modifie les adresses de retour de l'email.
        :param new_reply_to: Nouvelle adresse email de réponse du mail (string).
        :param new_return_path: Nouvelle adresse email de retour du mail en cas d'erreur (string).
        """
        self.set_item("Return-Path", return_path)

    def set_reply_to(self, reply_to):
        """
        Modifie les adresses de retour de l'email.
        :param new_reply_to: Nouvelle adresse email de réponse du mail (string).
        :param new_return_path: Nouvelle adresse email de retour du mail en cas d'erreur (string).
        """
        self.set_item("Reply-To", reply_to)

    @with_recipient_list
    def add_recipient(self, recipient, field_name):
        """
        Ajoute un destinataire à un champ spécifique (To, Cc, ou Bcc).
        :param recipient: Adresse email du destinataire (string).
        :param field_name: Champ de destinataire.
        """
        if field_name not in ["To", "Cc", "Bcc"]:
            raise ValueError(
                "Le champ de destinataire doit être 'To', 'Cc', ou 'Bcc'")
        # list_current_recipients = self.eml_object.eml_data[field_name]
        field_name = ModifyEml.convert_field_name(field_name)
        _bool = self.value_exist_in_field(self.eml_object, field_name)

        if _bool is True:
            # list_current_recipients = self.eml_object.eml_data[field_name]
            list_current_recipients = self.eml_object[field_name]
            # Utilisation d'une virgule comme séparateur
            current_recipients = ",".join(list_current_recipients)
            if recipient is not None:
                new_recipients = f"{current_recipients}, {recipient}"
            else:
                new_recipients = recipient
            self.set_item(field_name, new_recipients)

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

    # Obtenir la date en suivant le fuseau horaire et le changement d'heure

    def get_date(self, timezone_str="Europe/Paris"):
        local_tz = pytz.timezone(timezone_str)
        datetime_now = datetime.now(local_tz)

        # Formater la date selon le format RFC 2822 pour l’en-tête email
        return format_datetime(datetime_now)

    # Changer la date en suivant le fuseau horaire et le changement d'heure
    def set_date(self, timezone_str="Europe/Paris"):
        new_date = self.get_date(timezone_str)
        # Mettre à jour l'en-tête "Date"
        self.set_item("Date", new_date)

    def set_message_id(self):
        """
        Générer un nouvel identifiant unique.
        Modifie le champ 'Message-ID' de l'email.
        :param new_message_id: Nouveau Message-ID pour l'email (string).
        """
        # Générer un Message-ID unique
        new_message_id = make_msgid()

        # Remplacer le Message-ID de l'email
        self.set_item("Message-ID", new_message_id)

    def save(self, new_file_path):
        if not hasattr(self.eml_object, "as_bytes"):
            raise AttributeError(
                "L'objet EML ne possède pas de méthode 'as_bytes'.")
        with open(new_file_path, "wb") as f:
            f.write(self.eml_object.as_bytes())
