import unittest
from unittest.mock import patch, MagicMock
from email.message import EmailMessage
import os
from eml import Eml, EmlModifier 

class TestEml(unittest.TestCase):
    def setUp(self):
        # Créer un fichier .eml de test avec du contenu fictif
        self.test_file_path = 'test_email.eml'
        self.email_content = (
            "From: test.sender@example.com\n"
            "To: test.recipient@example.com\n"
            "Cc: cc.recipient@example.com\n"
            "Bcc: bcc.recipient@example.com\n"
            "Reply-To: replyto@example.com\n"
            "Return-Path: returnpath@example.com\n"
            "Date: Wed, 2 Oct 2021 14:30:00 +0000\n"
             
            "Message-ID: <test.message.id@example.com>\n"
            "Subject: Test Email\n\n"
            "This is a test email body."
        )
        
        with open(self.test_file_path, 'w', encoding='utf-8') as f:
            f.write(self.email_content)

        self.eml = Eml(self.test_file_path)

    def tearDown(self):
        # Supprimer le fichier de test après les tests
        if os.path.exists(self.test_file_path):
            os.remove(self.test_file_path)

    def test_get_metadata(self):
        # Vérifie que chaque champ est correctement extrait du fichier
        self.assertEqual(self.eml.get_sender(), 'test.sender@example.com')
        self.assertEqual(self.eml.get_to(), ['test.recipient@example.com'])
        self.assertEqual(self.eml.get_cc(), ['cc.recipient@example.com'])
        self.assertEqual(self.eml.get_bcc(), ['bcc.recipient@example.com'])
        self.assertEqual(self.eml.get_reply_to(), 'replyto@example.com')
        self.assertEqual(self.eml.get_return_path(), 'returnpath@example.com')
        self.assertEqual(self.eml.get_date(), 'Wed, 2 Oct 2021 14:30:00 +0000')
        self.assertEqual(self.eml.get_message_id(), '<test.message.id@example.com>')
        self.assertEqual(self.eml.get_subject(), 'Test Email')

    def test_print_eml(self):
        # Vérifie que la méthode d'affichage ne génère pas d'erreurs
        with patch('builtins.print') as mocked_print:
            self.eml.print_eml()
            mocked_print.assert_called()

    def test_get_name(self):
        # Vérifie que le nom de fichier est correctement extrait
        self.assertEqual(self.eml.get_name(), 'test_email.eml')

class TestEmlModifier(unittest.TestCase):
    def setUp(self):
        self.email_message = EmailMessage()
        self.email_message['From'] = 'test.sender@example.com'
        self.email_message['To'] = 'test.recipient@example.com'
        self.email_message['Cc'] = 'cc.recipient@example.com'
        self.email_message['Bcc'] = 'bcc.recipient@example.com'
        self.email_message['Reply-To'] = 'replyto@example.com'
        self.email_message['Return-Path'] = 'returnpath@example.com'
        self.email_message['Subject'] = 'Test Email'

        self.mock_eml = MagicMock()
        self.mock_eml._loaded_eml = self.email_message

        self.eml_modifier = EmlModifier(self.mock_eml)

    def test_set_sender(self):
        new_sender = 'new.sender@example.com'
        self.eml_modifier.set_sender(new_sender)
        self.assertEqual(self.mock_eml._loaded_eml['From'], new_sender)

    def test_set_return(self):
        new_reply_to = 'new.replyto@example.com'
        new_return_path = 'new.returnpath@example.com'
        self.eml_modifier.set_return(new_reply_to, new_return_path)
        self.assertEqual(self.mock_eml._loaded_eml['Reply-To'], new_reply_to)
        self.assertEqual(self.mock_eml._loaded_eml['Return-Path'], new_return_path)

    def test_add_recipient(self):
        new_recipient = 'new.recipient@example.com'
        self.eml_modifier.add_recipient(new_recipient, 'To')
        self.assertIn(new_recipient, self.mock_eml._loaded_eml['To'])

    def test_set_recipients(self):
        new_recipients = ['new1@example.com', 'new2@example.com']
        self.eml_modifier.set_recipients(new_recipients, 'Cc')
        self.assertEqual(self.mock_eml._loaded_eml['Cc'], ', '.join(new_recipients))

    def test_remove_recipient(self):
        self.eml_modifier.remove_recipient('cc.recipient@example.com', 'Cc')
        self.assertNotIn('cc.recipient@example.com', self.mock_eml._loaded_eml['Cc'])

    def test_remove_all_recipient(self):
        # Ajouter le même destinataire dans les champs "To", "Cc" et "Bcc"
        self.mock_eml._loaded_eml['To'] = 'test.recipient@example.com, duplicate@example.com'
        self.mock_eml._loaded_eml['Cc'] = 'cc.recipient@example.com, duplicate@example.com'
        self.mock_eml._loaded_eml['Bcc'] = 'bcc.recipient@example.com, duplicate@example.com'
        
        # Supprimer le destinataire commun
        self.eml_modifier.remove_all_recipient('duplicate@example.com')
        
        # Vérifier qu'il est bien supprimé de tous les champs
        self.assertNotIn('duplicate@example.com', self.mock_eml._loaded_eml['To'])
        self.assertNotIn('duplicate@example.com', self.mock_eml._loaded_eml['Cc'])
        self.assertNotIn('duplicate@example.com', self.mock_eml._loaded_eml['Bcc'])

    def test_get_email_message(self):
        # Vérifie que l'objet email retourné correspond bien à l'email modifié
        self.assertEqual(self.eml_modifier.get_email_message(), self.mock_eml._loaded_eml)

if __name__ == '__main__':
    unittest.main()
