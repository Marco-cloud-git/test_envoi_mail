import email
import imaplib
import sys
import time


def connexion(serveur_imap: str, port_imap: int, email_adress: str, password: str):
    start = time.time()
    resultat_connexion = "KO"
    
    try:
        obj_imap = imaplib.IMAP4_SSL(host=serveur_imap, port=port_imap)
        resultat_connexion, resultat_login = obj_imap.login(email_adress, password)
        
        if "OK" in resultat_connexion:
            print(f"Connexion à {email_adress} établie.")
        
        if "completed" in resultat_login[0].decode():
            print("Authentification réussie.")

        mssg_connection_object = f"Connection Object: {obj_imap}"
        mssg_total_time_taken = f"Total Time Taken: {time.time() - start:.2f} Seconds\n"
        print(f"{mssg_connection_object}\n{mssg_total_time_taken}")
        return obj_imap

    except Exception as e:
        print(f"Erreur de type : {type(e).__name__}, Erreur : {e}.")
    
    finally:
        if "OK" not in resultat_connexion or "completed" not in resultat_login[0].decode():
            print("Arrêt du script.")
            sys.exit()


def listerDossier(obj_imap: imaplib.IMAP4_SSL) -> None:
    try:
        mailBoxlist = []
        result, folders = obj_imap.list()
        
        for folder in folders:
            mailBoxlist.append(folder.decode("utf-8").split(' "/" ')[1])
        
        return mailBoxlist
    except Exception as e:
        print(f"Erreur lors de la récupération des dossiers : {e}.")
        sys.exit()


def count_mail_from_mailbox(obj_imap: imaplib.IMAP4_SSL, mailboxes: list[str]) -> None:
    try:
        for mailBox in mailboxes:
            response, value = obj_imap.select(mailBox)
            print(f"Sélection {mailBox} \t status {response}  \t nombre d'emails {value[0].decode()}.")
    except Exception as e:
        print(f"{mailBox} - Erreur : {type(e).__name__}, Message : {e}.")


def deconnexion(obj_imap: imaplib.IMAP4_SSL) -> None:
    try:
        if obj_imap is None:
            raise Exception("Erreur lors de la déconnexion car la connexion n'a pas été établie.")
        obj_imap.logout()
        print("Déconnexion réussie.")
    except imaplib.IMAP4_SSL.error as e:
        print(f"Erreur lors de la déconnexion : {e}.")


def listerUidMail(obj_imap: imaplib.IMAP4_SSL, mailBox: str) -> list[str]:
    obj_imap.select(mailBox)
    result, data = obj_imap.uid("search", None, "All")
    listUid = data[0].split()
    return listUid


def select_mailbox(obj_imap: imaplib.IMAP4_SSL, mailBox: str) -> str:
    try:
        resp_code, m_c = obj_imap.select(mailBox, readonly=True)
        return f"Réussite de la sélection du dossier {mailBox}, {resp_code}, {m_c}."
    except Exception as e:
        return f"Echec de la sélection du dossier : {mailBox}, Erreur : {type(e).__name__}, {e}."


def listerMail(obj_imap: imaplib.IMAP4_SSL, mailBox: str) -> list[str]:
    select_mailbox(obj_imap, mailBox)
    result, l = obj_imap.search(None, "All")
    listNumber = l[0].split()
    return listNumber


def lireMail(obj_imap: imaplib.IMAP4_SSL, mailBox: str, position: int, contenu="non") -> None:
    try:
        obj_imap.select(mailBox)
        l = listerMail(obj_imap, mailBox)
        n = position - 1
        result, email_data = obj_imap.fetch(l[n], "(RFC822)")
        raw_email = email_data[0][1]
        email_message = email.message_from_bytes(raw_email)

        from_ = email_message["From"]
        to_ = email_message["To"]
        cc_ = email_message["Cc"]
        bcc_ = email_message["Bcc"]
        subject_ = email_message["Subject"]
        date_ = email_message["Date"]
        messageId_ = email_message["Message-ID"]
        
        print(f"Message Number: {position}")
        print(f"From: {from_}")
        print(f"To: {to_}")
        print(f"Cc: {cc_}")
        print(f"Bcc: {bcc_}")
        print(f"Subject: {subject_}")
        print(f"Date: {date_}")
        print(f"Message-ID: {messageId_}")
        
        contenu = contenu.lower()
        if contenu == "oui":
            afficherContenu(email_message)
        elif contenu not in ["non", None]:
            print("contenu ne peut prendre que les valeurs 'oui' ou 'non'.")
            raise ValueError("La valeur de l'argument doit être 'oui' ou 'non'.")

    except Exception as e:
        print(f"Erreur lors de la lecture du mail à la position {position}\nErreur : {e}.")


def afficherContenu(email_message) -> None:
    print("\nContenu:")
    if email_message.is_multipart():
        text = ""
        for part in email_message.walk():
            if part.get_content_type() == "text/plain":
                payload = part.get_payload(decode=True)
                if payload is not None:
                    charset = part.get_content_charset()
                    if charset:
                        text += payload.decode(charset).replace("\r", "")
            elif part.get_content_type() != "multipart/alternative":
                continue
    else:
        text = email_message.get_payload(decode=True)
        charset = email_message.get_content_charset()
        if charset:
            text = text.decode(charset).replace("\r", "")
    
    print(text)


def importEml(path_eml: str, server: str, mailbox: str) -> None:
    try:
        data = eml_binary(path_eml)
        date = imaplib.Time2Internaldate(time.time())
        rc, response = server.append(mailbox, "", date, data)
        
        mssg = (
            f"Chemin de l'eml à copier : {path_eml}\n"
            f"Mailbox : {mailbox}\n"
            f"Date : {date}\n"
            f"Status : {rc}\n"
            f"Réponse : {response}.\n"
        )
        print(mssg)

    except Exception as e:
        print(f"Echec de l'importation de l'eml : {path_eml}\nErreur : {e}.")


def eml_binary(pathFile: str) -> bytes:
    try:
        with open(pathFile, "rb") as f:
            return f.read()
    except Exception as e:
        print(f"Echec de l'ouverture du fichier : {pathFile}, Erreur : {e}")



