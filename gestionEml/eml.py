#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email import policy
from email.parser import BytesParser
from email.utils import format_datetime, make_msgid
from os import path
from pathlib import Path
from datetime import datetime
import pytz
from functools import wraps
from email.header import decode_header

from gestionEml.emlUtils import define_file_path, increment_file_name


class Eml:
    def __init__(self, file_path):
        self.file_path = file_path
        self.eml_data = self.load_eml(file_path)
        self.get_data()

    def load_eml(self, file_path):
        """
        Ouvrir un fichier eml en mode binaire et permettre l'analyse.
        :param file_path: chemin vers le fichier (string).
        """
        with open(file_path, "rb") as f:
            return BytesParser(policy=policy.default).parse(f)

    def get_data(self):
        """
        Déclaration de tous les paramètres du header de l'eml dans l'instance
        """
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
            if item.startswith("_"):
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
        return path.basename(self.file_path)

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
        Methode pour lire les valeurs des champs To, CC et Bcc.
        Retourne une liste.
        :param field_name: nom du champs (string).
        """
        addresses = self.eml_data[field_name]
        if addresses:
            return [TextEncoding.decode_header(addr) for addr in addresses.split(", ")]
        return []

    def as_bytes(self):
        return self.eml_data.as_bytes()


class ModifyEml:
    def __init__(self, eml_object):
        """
        Initialise l'objet avec les valeurs issus de la classe Eml,
        contient file_path : chemin vers l'eml,
        eml_data : texte de l'eml,
        name : nom de l'eml,
        paramètress extraits du header :  sender,  to, cc, bcc, reply_to, return_path, date, message_id, subject.
        """
        if eml_object is None:
            raise ValueError("L'objet eml fourni est None.")
        else:
            self.eml_object = eml_object  # Composition : `ModifyEml` contient `Eml`

    def with_recipient_list(func):
        """
        decorateur pour gérer et modifier les adresses mails de destination dans le cas d'une liste.
        """

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

    def _convert_field_name(field):
        """
        Converti les noms de certains champs des emls en parametres de l'objet eml_objet de l'instance.
        :param field : nom du champs de l'eml à convertir (string).
        """
        if field in [
            "To",
            "Cc",
            "Bcc",
            "From",
            "Return-Path",
            "Reply-To",
            "Date",
            "Subject",
            "Message-ID",
        ]:
            switch = {
                "To": "to",
                "Cc": "cc",
                "Bcc": "bcc",
                "From": "sender",
                "Return-Path": "return_path",
                "Reply-To": "reply_to",
                "Date": "date",
                "Subject": "subject",
                "Message-ID": "message_id",
            }
            return switch.get(field, "Not a field")
        else:
            return field

    def _value_exists(self, field):
        """
        Test si le champs existe dans eml_object d'une instance.
        Retourne un booléen correspond au test et la valeur obtenue.
        Ceci évite de rechercher dans le texte du mail si le champs existe et de perdre du temps à obtenir la valeur.
        :param field: le champs à tester (string).
        """
        exists = False
        value = None
        if field is not None:
            value = getattr(self.eml_object, field, None)
            if isinstance(value, list) or isinstance(value, tuple):
                value = ", ".join(value).strip()
            if value is not None and len(value) > 0:
                exists = True
        return exists, value

    def _already_exists(value, list_adresses):
        """
        Test si la valeur n'existe pas dans une liste.
        list_adresses est converti en liste si c'est une chaine de caractère.
        Retourne un booléen.
        :param value: valeur à tester (string ou liste).
        :param list_adresses: liste d'adresses à comparer.
        """
        exists = False

        if value is not None:
            if isinstance(list_adresses, str):
                list_adresses = ModifyEml.parse_email_list(list_adresses)

            if isinstance(list_adresses, list) or isinstance(list_adresses, tuple):
                exists = value in list_adresses
        return exists

    def update_header_field(self, field):
        """
        Modifie la valeur d'une balise dans le header de l'email.
        La valeur doit exister dans l'instance et la nouvelle valeur ne doit pas etre nulle.
        :param field: nom du champs à modifier (string).
        """
        item = ModifyEml._convert_field_name(field)
        exists, value = self._value_exists(item)
        if exists is True and value is not None:
            self.eml_object.eml_data.replace_header(field, value)

    def parse_email_list(adress):
        """
        Permet de découper la chaine de caractère contenant les adresses mails.
        Retourne une liste d'adresses.
        :param recipient: une ou plusieurs adresses mails
        """
        return list(map(str.strip, adress.split(",")))

    @with_recipient_list
    def _add_recipient(self, recipient, field_name):
        """
        Ajoute un destinataire à un champ spécifique (To, Cc, ou Bcc).
        L'ajout ne se fait que si la valeur n'existe pas déjà.
        :param recipient: Adresse email du destinataire (string).
        :param field_name: Champ de destinataire.
        """
        if not field_name in ["To", "Cc", "Bcc"]:
            msg = f'field_name : {field_name} doit être : "To", "Cc", "Bcc".'
            raise ValueError(msg)
        convert_field = ModifyEml._convert_field_name(field_name)
        exists, list_current_recipients = self._value_exists(convert_field)
        recipient_already_exists = ModifyEml._already_exists(
            value=recipient, list_adresses=list_current_recipients
        )

        if exists is True and recipient_already_exists is False:
            if recipient is not None:
                new_recipients = f"{list_current_recipients}, {recipient}"
            else:
                new_recipients = recipient
            self._set_item(value=new_recipients, field=convert_field)

    def add_to(self, recipient):
        """
        Ajoute un destinataire au champ To.
        L'ajout ne se fait que si la valeur n'existe pas déjà.
        :param recipient: Adresse email du destinataire (string).
        """
        self._add_recipient(recipient=recipient, field_name="To")

    def add_cc(self, recipient):
        """
        Ajoute un destinataire au champ Cc.
        L'ajout ne se fait que si la valeur n'existe pas déjà.
        :param recipient: Adresse email du destinataire (string).
        """
        self._add_recipient(recipient=recipient, field_name="Cc")

    def add_bcc(self, recipient):
        """
        Ajoute un destinataire au champ Bcc.
        L'ajout ne se fait que si la valeur n'existe pas déjà.
        :param recipient: Adresse email du destinataire (string).
        """
        self._add_recipient(recipient=recipient, field_name="Bcc")

    def _remove_recipient(self, recipient, field_name):
        """
        Supprime un destinataire spécifique d'un champ (To, Cc, ou Bcc).
        :param recipient: Adresse email du destinataire à supprimer (string).
        :param field_name: Champ de destinataire où chercher l'adresse.
        """
        convert_field = ModifyEml._convert_field_name(field_name)
        exists, value = self._value_exists(convert_field)
        if exists is True and value is not None:
            # transforme la valeur value en list
            list_value = ModifyEml.parse_email_list(value)
            list_new_recipients = [
                x for x in list_value if x != recipient
            ]  # Ne fait rien, pas d'erreur
            # transforme la liste modifié en string
            new_recipients = ", ".join(list_new_recipients).strip()
            return self._set_item(value=new_recipients, field=convert_field)

    def remove_to(self, recipient):
        """
        Supprime un destinataire spécifique d'un champ To.
        :param recipient: Adresse email du destinataire à supprimer (string).
        """
        self._remove_recipient(recipient, field_name="To")

    def remove_cc(self, recipient):
        """
        Supprime un destinataire spécifique d'un champ Cc.
        :param recipient: Adresse email du destinataire à supprimer (string).
        """
        self._remove_recipient(recipient, field_name="Cc")

    def remove_bcc(self, recipient):
        """
        Supprime un destinataire spécifique d'un champ Bcc.
        :param recipient: Adresse email du destinataire à supprimer (string).
        """
        self._remove_recipient(recipient, field_name="Bcc")

    def _set_item(self, value, field):
        """
        Modifie la valeur d'un paramétre dans l'instance.
        La valeur doit exister dans l'instance et la nouvelle valeur ne doit pas etre nulle.
        :param field: nom du champs à modifier (string).
        :param value: nouvelle valeur de la balise (string).
        """
        exists, _ = self._value_exists(field)
        if exists is True and value is not None:
            setattr(self.eml_object, field, value)

    def _set_recipient(self, recipient, field_name):
        """
        Remplace les destinataires d'un champ spécifique (To, Cc, ou Bcc).
        :param recipient: adresses email (string).
        :param field_name: Champ de destinataire à modifier (string).
        """
        convert_field = ModifyEml._convert_field_name(field_name)
        self._set_item(value=recipient, field=convert_field)

    def set_subject(self, subject):
        """
        Modifie dans l'instance le sujet de l'email.
        :param subject: Nouveau sujet de l'email.
        """
        self._set_item(value=subject, field="subject")

    def set_from(self, sender):
        """
        Modifie dans l'instance l'expéditeur de l'email.
        :param sender: Nouvelle adresse email de l'expéditeur (string).
        """
        self._set_item(value=sender, field="sender")

    def set_return_path(self, return_path):
        """
        Modifie dans l'instance les adresses de retour de l'email.
        :param return_path: Nouvelle adresse email de retour du mail en cas d'erreur (string).
        """
        self._set_item(value=return_path, field="return_path")

    def set_reply_to(self, reply_to):
        """
        Modifie dans l'instance les adresses de retour de l'email.
        :param reply_to: Nouvelle adresse email de réponse du mail (string).
        """
        self._set_item(value=reply_to, field="reply_to")

    def set_to(self, recipient):
        """
        Remplace les destinataires du champ To.
        :param recipient: adresses email (string).
        """
        self._set_recipient(recipient, field_name="To")

    def set_cc(self, recipient):
        """
        Remplace les destinataires du champ Cc.
        :param recipient: adresses email (string).
        """
        self._set_recipient(recipient, field_name="Cc")

    def set_bcc(self, recipient):
        """
        Remplace les destinataires du champ Bcc.
        :param recipient: adresses email (string).
        """
        self._set_recipient(recipient, field_name="Bcc")

    # Changer la date en suivant le fuseau horaire et le changement d'heure
    def set_date(self, timezone_str="Europe/Paris"):
        """
        Permet d'enregistrer la date actuel dans l'instance.
        Prend en compte la time zone.
        """
        local_tz = pytz.timezone(timezone_str)
        datetime_now = datetime.now(local_tz)
        new_date = format_datetime(datetime_now)
        # Mettre à jour l'en-tête "Date"
        self._set_item(value=new_date, field="date")

    def set_message_id(self):
        """
        Génére un nouvel identifiant unique.
        Modifie le champ 'Message-ID' de l'instance.
        """
        # Générer un Message-ID unique
        new_message_id = make_msgid()
        # Remplacer le Message-ID de l'email
        self._set_item(value=new_message_id, field="message_id")

    def _modify_header(
        self,
    ):
        """
        Modifie dans eml_data (texte de l'eml) le sujet, les adresses de l'expediteur, du reply-to, du return_path de l'email, du destinataire principale, du destinataire secondaire, du destinataire caché, de la date et du message_id.
        La modification de la date dans l'instance est faite obligatoirement ici.
        Une boucle permet de modifier dans eml_data les valaurs de : Date, Message-ID, Subject, From, Return-Path, Reply-To, To, Cc, Bcc.
        """
        self.set_date(timezone_str="Europe/Paris")

        for item in [
            "Date",
            "Message-ID",
            "Subject",
            "From",
            "Return-Path",
            "Reply-To",
            "To",
            "Cc",
            "Bcc",
        ]:
            self.update_header_field(item)

    def save(self, file_path, increment=1000):
        """
        Enregistrer un objet email au format eml.
        :param new_file_path: chemin de destination de l'eml.
        """
        self._modify_header()
        if not hasattr(self.eml_object, "as_bytes"):
            raise AttributeError("L'objet eml ne possède pas de méthode 'as_bytes'.")
        new_file_path, new_file_name = increment_file_name(file_path, increment)
        with open(new_file_path, "wb") as f:
            f.write(self.eml_object.as_bytes())
        return new_file_path, new_file_name


def modify(
    file_path,
    destination_folder,
    subject=None,
    sender=None,
    return_path=None,
    reply_to=None,
    to=None,
    cc=None,
    bcc=None,
    message_id=True,
):
    """
    Fonction simple pour modifier les emls.
    Ne prend en charge que les fonctions set, mais pas add ou remove.
    Retourne un tuple constitué de date, message_id, original_file_name, new_file_path, new_file_name.
    :param file_path: chemin vers l'eml (string).
    :param destination_folder: chemin vers le dossier de destination de l'eml pour la sauvegarde (string).
    :param subject: valeur du sujet du mail à modifier,None par défaut (string).
    :param sender: valeur de l'expéditeur (From) du mail à modifier, None par défaut (string).
    :param return_path: valeur de réponse en cas d'erreur à modifier, None par défaut (string).
    :param reply_to: valeur de réponse du mail à modifier, None par défaut (string).
    :param to: valeur du destinataire principale du mail à modifier, None par défaut (string).
    :param cc: valeur du destinataire secondaire du mail à modifier, None par défaut (string).
    :param bcc: valeur du destinataire caché du mail à modifier, None par défaut (string).
    :param message_id: True permet de modifier le Message-ID, True par défaut (boolean).
    """
    # Charger l'email d'entrée
    eml = Eml(file_path)
    # Eml.print_eml_data(eml, eml_data=False)
    original_file_name = eml.get_name()
    # # Construire le chemin de destination et sauvegarder
    destination_file_path = path.join(destination_folder, original_file_name)
    destination_file_path = Path(destination_file_path)
    # Créer l'objet à modifier
    eml_modifier = ModifyEml(eml)
    # modifier les valeurs

    eml_modifier.set_subject(subject)
    eml_modifier.set_from(sender)
    eml_modifier.set_return_path(return_path)
    eml_modifier.set_reply_to(reply_to)
    eml_modifier.set_to(to)
    eml_modifier.set_cc(cc)
    eml_modifier.set_bcc(bcc)

    if message_id == True:
        eml_modifier.set_message_id()

    new_file_path, new_file_name = eml_modifier.save(destination_file_path)

    # obtenir les informations nécessaires pour les tests
    date = eml.get_date()
    message_id = eml.get_message_id()
    return date, message_id, original_file_name, new_file_path, new_file_name


def execute_eml_modification(
    process, file_name, entry_folder_path, destination_folder_path
):
    """
    Traite la modification des fichiers eml en fonction du nom de fichier fourni.
    Retourne une liste de dictionaire contenant constitué d'un dictionnaire avec date, message_id, original_file_name, new_file_path, new_file_name.
    :param process: Fonction à appliquer au fichier eml (string).
    :param file_name: Nom de fichier ou liste de noms de fichiers eml à traiter (string ou list).
    :param entry_folder_path: Chemin du dossier d'entrée (string).
    :param destination_folder_path: Chemin du dossier de destination (string).
    """
    list_value = []

    if isinstance(file_name, list) or isinstance(file_name, tuple):
        for name in file_name:
            try:
                date, message_id, original_file_name, new_file_path, new_file_name = (
                    _modify_eml(
                        process=process,
                        file_name=name,
                        entry_folder_path=entry_folder_path,
                        destination_folder_path=destination_folder_path,
                    )
                )
                dictionary = {
                    "date": date,
                    "message_id": message_id,
                    "original_file_name": original_file_name,
                    "new_file_path": new_file_path,
                    "new_file_name": new_file_name,
                }
                list_value.append(dictionary)
            except Exception as e:
                msg = f"Erreur lors du traitement de l'eml {name}: {e}"
                print(msg)
    elif isinstance(file_name, str):
        try:
            date, message_id, original_file_name, new_file_path, new_file_name = (
                _modify_eml(
                    process=process,
                    file_name=file_name,
                    entry_folder_path=entry_folder_path,
                    destination_folder_path=destination_folder_path,
                )
            )
            dictionary = {
                "date": date,
                "message_id": message_id,
                "original_file_name": original_file_name,
                "new_file_path": new_file_path,
                "new_file_name": new_file_name,
            }
            list_value.append(dictionary)
        except Exception as e:
            msg = f"Erreur lors du traitement de l'eml {file_name}: {e}"
            print(msg)
    else:
        msg = f"Erreur lors du traitement de l'eml {file_name}: {e}"
        raise ValueError(msg)
    return list_value


def _modify_eml(process, file_name, entry_folder_path, destination_folder_path):
    """
    Modifie un fichier eml en utilisant la fonction de traitement fournie.
    Retourne un tuple constitué de date, message_id, original_file_name, new_file_path, new_file_name.
    :param process: Fonction à appliquer au fichier eml.
    :param file_name: Nom du fichier eml à traiter (string).
    :param entry_folder_path: Chemin du dossier d'entrée (string).
    :param destination_folder_path: Chemin du dossier de destination (string).
    """

    if file_name is not None:
        file_path = define_file_path(
            directory_path=entry_folder_path, file_name=file_name
        )
    else:
        msg = f"Erreur sur file_name : {file_name}"
        raise ValueError(msg)

    date, message_id, original_file_name, new_file_path, new_file_name = (
        _wrapper_process(
            process=process,
            file_path=file_path,
            destination_folder_path=destination_folder_path,
        )
    )
    return date, message_id, original_file_name, new_file_path, new_file_name


def _wrapper_process(process, file_path, destination_folder_path):
    """
    Wrapper pour appeler les fonctions de traitement.
    Retourne un tuple constitué de date, message_id, original_file_name, new_file_path, new_file_name.
    :param process: Fonction à appliquer au fichier eml (string).
    :param file_path: Chemin du fichier eml à traiter (string).
    :param destination_folder_path: Chemin du dossier de destination (string).
    """
    date, message_id, original_file_name, new_file_path, new_file_name = process(
        eml_file_path=file_path, destination_folder_path=destination_folder_path
    )
    return date, message_id, original_file_name, new_file_path, new_file_name


class TextEncoding:
    @staticmethod
    def decode_header(encoded_string):
        """
        Permet de lire les valeurs éventuellement encondés contenu dans le header des emls.
        64 bits :  caractères alphanumériques et de symboles (+, /, =) pour représenter les octets binaires, ex : SGVsbG8gd29ybGQh
        Quoted-Printable : caractères ASCII suivis d’un “=” suivi d’un chiffre hexadécimal représentant le code Unicode du caractère original, ex : =?iso-8859-1?q?école=?
        UTF-8 : peuvent contenir des caractères tels que des accents, des diacritiques, des caractères spéciaux, ainsi que des symboles et des lettres non latines, ex : \xc3\xa9cole

        """
        # Vérifier si la chaîne est None avant le décodage
        if encoded_string is None:
            return ""  # Retourne une chaîne vide si l'en-tête n'existe pas
        decoded_fragments = []
        for part, encoding in decode_header(encoded_string):
            if isinstance(part, bytes):
                decoded_fragments.append(part.decode(encoding or "utf-8"))
            else:
                decoded_fragments.append(part)
        return "".join(decoded_fragments)


class InvalidEncodingError(Exception):
    """A custom exception class to report Invalid Encoding errors."""

    def __init__(self, encoded_value: str = ""):
        self.encoded_value = encoded_value
        self.message = "Invalid encoding used"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}. Encoded string causing the error: {self.encoded_value}"
