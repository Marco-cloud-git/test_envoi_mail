#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests de la classe Eml :
Vérifier que le fichier EML est chargé correctement.
Vérifier que les méthodes de récupération (get_name, get_sender, get_to, etc.) fonctionnent comme attendu.

Tests de la classe ModifyEml :
Vérifier les méthodes de modification de destinataires (add_to, add_cc, add_bcc, etc.).
Tester les méthodes de suppression de destinataires (remove_to, remove_cc, remove_bcc).
Vérifier les modifications du header de l'email.

Tests de la classe TextEncoding :
Tester le décodage d’en-têtes codés (en base64, quoted-printable, UTF-8).

Tests de la classe InvalidEncodingError :
Vérifier le comportement de cette exception personnalisée.
"""

import unittest
from unittest.mock import Mock, patch, mock_open
from email.message import EmailMessage
import pytz
from datetime import datetime
from eml import Eml, ModifyEml, TextEncoding, InvalidEncodingError


class TestEml(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="From: test@example.com\nTo: user@example.com\nSubject: Test")
    def test_load_eml(self, mock_file):
        eml = Eml("dummy.eml")
        self.assertIsInstance(eml.eml_data, EmailMessage)

    @patch("builtins.open", new_callable=mock_open, read_data="From: test@example.com\nTo: user@example.com\nSubject: Test")
    def test_get_name(self, mock_file):
        eml = Eml("dummy.eml")
        self.assertEqual(eml.get_name(), "dummy.eml")

    @patch("builtins.open", new_callable=mock_open, read_data="From: test@example.com\nTo: user@example.com\nSubject: Test")
    def test_get_sender(self, mock_file):
        eml = Eml("dummy.eml")
        self.assertEqual(eml.get_sender(), "test@example.com")

    @patch("builtins.open", new_callable=mock_open, read_data="From: test@example.com\nTo: user@example.com\nSubject: Test")
    def test_get_to(self, mock_file):
        eml = Eml("dummy.eml")
        self.assertEqual(eml.get_to(), ["user@example.com"])


class TestModifyEml(unittest.TestCase):
    def setUp(self):
        eml = Mock(spec=Eml)
        eml.file_path = "dummy.eml"
        eml.sender = "test@example.com"
        eml.to = ["user@example.com"]
        self.modifier = ModifyEml(eml)

    def test_add_to(self):
        self.modifier.add_to("new@example.com")
        self.assertIn("new@example.com", self.modifier.eml_object.to)

    def test_remove_to(self):
        self.modifier.eml_object.to = ["user@example.com", "other@example.com"]
        self.modifier.remove_to("other@example.com")
        self.assertNotIn("other@example.com", self.modifier.eml_object.to)

    @patch("datetime.datetime")
    def test_set_date(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 1, 1, 12, 0, tzinfo=pytz.timezone("Europe/Paris"))
        self.modifier.set_date()
        self.assertIn("2023", self.modifier.eml_object.date)


class TestTextEncoding(unittest.TestCase):
    def test_decode_header_base64(self):
        encoded = "=?utf-8?b?SGVsbG8gd29ybGQ=?="
        self.assertEqual(TextEncoding.decode_header(encoded), "Hello world")

    def test_decode_header_quoted_printable(self):
        encoded = "=?iso-8859-1?q?=E9cole?="
        self.assertEqual(TextEncoding.decode_header(encoded), "école")

    def test_decode_header_utf8(self):
        encoded = "\xc3\xa9cole"
        self.assertEqual(TextEncoding.decode_header(encoded), "école")


class TestInvalidEncodingError(unittest.TestCase):
    def test_invalid_encoding_error(self):
        error = InvalidEncodingError("invalid_encoding_string")
        self.assertEqual(str(error), "Invalid encoding used. Encoded string causing the error: invalid_encoding_string")


if __name__ == "__main__":
    unittest.main()
