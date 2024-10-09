#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from eml import Eml


file_path="depot_eml/test YAHOO PJ nom avec caractères spéciaux.eml"

def main(file_path):
    eml = Eml(file_path)
    print("Name:", eml.name)
    print("Sender:", eml.sender)
    print("To:", eml.to)
    print("Cc:", eml.cc)
    print("Bcc:", eml.bcc)
    print("Reply-To:", eml.reply_to)
    print("Return-Path:", eml.return_path)
    print("Date:", eml.date)
    print("Message-ID:", eml.message_id)
    print("Subject:", eml.subject)
    # print("Body:", eml.get_body())

if __name__ == "__main__":
    file_path = "depot_eml/test YAHOO PJ nom avec caractères spéciaux.eml"
    main(file_path)