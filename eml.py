#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from email import policy
from email.parser import BytesParser
import os
from text_encoding import TextEncoding


class Eml:
    def __init__(self, file_path):
        self.file_path = file_path
        self.message = self._load_eml(file_path)
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

    def _load_eml(self, file_path):
        with open(file_path, 'rb') as f:
            return BytesParser(policy=policy.default).parse(f)

    def get_name(self):
        return os.path.basename(self.file_path)

    def get_sender(self):
        return TextEncoding.decode_header(self.message['From'])

    def get_to(self):
        return self._get_addresses('To')

    def get_cc(self):
        return self._get_addresses('Cc')

    def get_bcc(self):
        return self._get_addresses('Bcc')

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
        try:
            if self.message.is_multipart():
                return ''.join(part.get_content() for part in self.message.iter_parts() if part.get_content_type() == 'text/plain')
            else:
                return self.message.get_body(preferencelist=('plain')).get_content()
        except Exception as e:
            print("Error retrieving body:", e)
            return None

    def _get_addresses(self, field_name):
        """
        Helper method to parse multiple email addresses in the To, Cc, and Bcc fields.
        """
        addresses = self.message[field_name]
        if addresses:
            return [TextEncoding.decode_header(addr) for addr in addresses.split(',')]
        return []

    def save(self, new_file_path=None):
        if new_file_path is None:
            new_file_path = self.file_path
        with open(new_file_path, 'wb') as f:
            f.write(self.message.as_bytes())
