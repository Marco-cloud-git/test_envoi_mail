#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# import email
from email import policy
from email.parser import BytesParser
import os
from text_encoding import TextEncoding

class Eml:
    def __init__(self, file_path):
        self.file_path = file_path
        self.message = Eml._load_eml(self, self.file_path)
        self.name = Eml.get_name(self)
        self.sender = Eml.get_sender(self)
        self.to = Eml.get_to(self)
        self.cc = Eml.get_cc(self)
        self.bcc = Eml.get_bcc(self)
        self.reply_to = Eml.get_reply_to(self)
        self.return_path = Eml.get_return_path(self)
        self.date = Eml.get_date(self)
        self.message_id = Eml.get_message_id(self)
        self.subject = Eml.get_subject(self)
        # self.body = Eml.get_body()

    def _load_eml(self, file_path):
        with open(file_path, 'rb') as f:
            return BytesParser(policy=policy.default).parse(f)

    def get_name(self):
        return os.path.basename(self.file_path)

    def get_sender(self):
        return TextEncoding.decode_header(self.message['From'])

    def get_to(self):
        return TextEncoding.decode_header(self.message['To'])
    
    def get_cc(self):
        return TextEncoding.decode_header(self.message['Cc'])
    
    def get_bcc(self):
        return TextEncoding.decode_header(self.message['Bcc'])
    
    def get_reply_to(self):
        return TextEncoding.decode_header(self.message['Reply-To'])

    def get_return_path(self):
        return TextEncoding.decode_header(self.message['Return-Path'])

    def get_date(self):
        return self.message['Date']

    def get_message_id(self):
        return self.message['Message-ID']
    
    def get_subject(self):
        return self.message['Subject']

    def get_body(self):
        # Gérer les différents types de contenu (texte brut, HTML)
        if self.message.is_multipart():
            return ''.join(part.get_content() for part in self.message.iter_parts() if part.get_content_type() == 'text/plain')
        else:
            return self.message.get_body(preferencelist=('plain')).get_content()

    def save(self, new_file_path=None):
        if new_file_path is None:
            new_file_path = self.file_path
        with open(new_file_path, 'wb') as f:
            f.write(self.message.as_bytes())



   
