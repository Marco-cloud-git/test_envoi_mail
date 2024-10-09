#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email.header import decode_header

class TextEncoding:
    @staticmethod
    def decode_header(encoded_string):
         # Vérifier si la chaîne est None avant le décodage
        if encoded_string is None:
            return ""  # Retourne une chaîne vide si l'en-tête n'existe pas
        decoded_fragments = []
        for part, encoding in decode_header(encoded_string):
            if isinstance(part, bytes):
                decoded_fragments.append(part.decode(encoding or 'utf-8'))
            else:
                decoded_fragments.append(part)
        return ''.join(decoded_fragments)

class InvalidEncodingError(Exception):
    """A custom exception class to report Invalid Encoding errors."""
    def __init__(self, encoded_value: str = ''):
        self.encoded_value = encoded_value
        self.message = "Invalid encoding used"
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message}. Encoded string causing the error: {self.encoded_value}"