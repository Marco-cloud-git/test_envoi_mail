from time import perf_counter
import gestionEml
import Imap.connexionIMAP as connexionIMAP
import os
import json

# from gestionLog import Report as Report


############### GESTION EML ###############
environnement = "recx"      #"recx"  #"tdv2"  "recn"    "ppcor" "preprod"

# 'auto' remplacement automatique de tous les parametres
# 'OUI' 'NON' obligatoire, non sensible à la casse
# 'NON' aucun remplacement
# 'OUI' remplacement de la valeur du message id et de la date plus les remplacements optionnels
modifierHeader = "oui"

# auto : remplace la valeur du From par une valeur par defaut (selon expedietur d'origine maif/non maif).
# autre: ("monadresse@example.com") remplace la valeur du From par la nouvelle valeur.
# None : aucun remplacement
# les valeur du return ,du reply et de sender sont automatiquement remplaces par la valeur du From si elles existent
sender = "resiliation@darva.com"

# auto : chercher une BAL GED dans les destinataires et modifier par une adresse de test equivalente
# pour les autres genere une adresse aleatoire et ajoute un domaine test.fr ou maif.fr selon le domaine
# autre: (["test1@example.com", "test2@example.com"]) remplace le To par la valeur de la liste
# None : aucun remplacement de To
to_list = "auto"  # ["test1@example.com", "test2@example.com"]

# auto : chercher une BAL GED dans les destinataires et modifier par une adresse de test equivalente
# pour les autres genere une adresse aleatoire et ajoute un domaine test.fr ou maif.fr selon le domaine
# autre: (["test3@example.com", "test4@example.com"]) remplace le Cc par la valeur de la liste
# None : aucun remplacement de Cc
cc_list = "auto"  # ["test3@example.com", "test4@example.com"]

# auto : chercher une BAL GED dans les destinataires et modifier par une adresse de test equivalente
# pour les autres genere une adresse aleatoire et ajoute un domaine test.fr ou maif.fr selon le domaine
# None : aucun remplacement de Bcc
# autre: (["test5@example.com", "test6@example.com"]) remplace le bcc par la valeur de la liste
bcc_list = "auto"  # ["test5@example.com", "test6@example.com"]

# auto : prend l'ancien sujet + ajout une référence aléatoire dans la liste au début + ajout date en fin 
# autre : (6420,  "Mon sujet de test") prend la valeur + date
# None : garde le sujet d'origine mais supprime les references
subject =  "Resiliation Darva - 2624910H"

# renomme le nom de l'eml
# auto : prend la valeur sujet + eml comme nouveau nom -> peut introduire des caractéres qui font peter la modification de l'eml
# autre : (1234, "test.eml") changement de nom par ces valeurs + eml
# None : garde le nom d'origine
name = None

# valeur pour l'import
# auto : prendre la valeur de la premiere BAL GED et faire l'import
# non : ne rien importer
# autre : prend la valeur comme bal d'import
importerEml = "non"

# definir les entrees/sorties
entree = "./entree"
sortie = "./sortie"
export = "./export"
test = "./entree/test"
autre = "./entree/autre"
mini = "./entree/mini"
anoExpediteur = "./entree/anomalie/expediteur"
envoi = "./entree/envoi"
testReturn = "./entree/anomalie/return"
destinatireMultiple = "./entree/destinataireMultiple"
annulation_ARs_logistiques = "./entree/Harmonication des ARs - Gestion des rejets SGDMail - Annulation des ARs logistiques"
priseContact = "./entree/demande de prise de contact"
supprimerCaracteresSpeciauxSujet = "./entree/Supprimer caracteres speciaux du sujet"
resilVente = './entree/resiliation/vente'
mails_domaine_sinistre = "./entree/mails domaine sinistre"
mails_domaine_societaire = "./entree/mails domaine societaire"
reclaSoc_maiffr = "./entree/Réclamations/contrat/eml"
reclaSin_maiffr = "./entree/Réclamations/sinistre/eml"
resil_darva = "./entree/resil_darva"


# reference:
# referenceSocietaire = "./reference/env/env_societaire"
# referenceEvenement = "./reference/env/env_evenement"
reference = "auto"

lire_eml = "lire"

# Parametrages IMAP
# "pptechimap.maif.pprod" #"outlook.office365.com"
imap_serveur = (
    "pptechimap.maif.pprod"  # "pptechimap.maif.pprod"  # "imap-mail.outlook.com"
)
port_imap = 993
# "gestionsinistre.recn.o365@pprodmaif.fr"
email_adress = "reclamation.ppcor.o365@pprodmaif.fr"  # "gestionsinistre.preprod.o365@pprodmaif.fr"       #"resiliationinternet.recx.o365@pprodmaif.fr"   #"gestionsocietaire.recn.o365@pprodmaif.fr"  # "rejet_mail.recn.o365@pprodmaif.fr"  # "jeandelaged@outlook.fr"
password = "GeDM@aif0365"  # "GedJean@extXXX"  # "GeDM@aif0365"


# chemin vers le dossier rapport
pathDir_rapport = "./rapport"

# chemin vers le dossier de log
# pathDir_log = "./log"


##### APPEL########
# en ligne de commande
# py start.py ou python .\start.py


if __name__ == "__main__":
    # se connecter
    imap = connexionIMAP.connexion(imap_serveur, port_imap, email_adress, password)

    # avoir la liste des dossier de la boite mail
    mailBoxlist = connexionIMAP.listerDossier(imap)

    # afficher la liste des dossiers    
    print(f"Liste des dossiers de la boite mail : {mailBoxlist}")

    # compter le nombre de mail dans la messagerie
    connexionIMAP.count_mail_from_mailbox(imap, mailBoxlist)

    # faire des listes d'identifiant de mail par dossier
    dossier_a_lire = "INBOX"      #"Brouillons"   #"INBOX"
    # liste des uuid    
    print(connexionIMAP.listerUidMail(imap, dossier_a_lire))
    # afficher une liste de mail dans un dossier
    # print(connexionIMAP.listerMail(imap, dossier_a_lire))
    

    # lire l'en tête d'un eml et afficher eventuellement le message pour un eml à une postion precise dans un dossier donne
    # 1)  # 1, "Oui") #1, "Non")
    # connexionIMAP.lireMail(imap, dossier_a_lire, 1, "Oui")

    # se deconnecter
    connexionIMAP.deconnexion(imap)