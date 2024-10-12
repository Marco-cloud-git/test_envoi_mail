#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from eml import Eml


file_path="depot_eml/test YAHOO PJ nom avec caractères spéciaux.eml"

def main(file_path):
    eml = Eml(file_path)
    Eml.print_eml(eml)

if __name__ == "__main__":
    file_path = "depot_eml/test YAHOO PJ nom avec caractères spéciaux.eml"
    main(file_path)