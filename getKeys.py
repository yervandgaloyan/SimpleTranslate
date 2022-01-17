#!/usr/bin/env python3
import re
import argparse


parser=argparse.ArgumentParser(
    description='Simple Translate. Created by Yervand Galoyan', 
    )

requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('--input', '-i', help='Input file name', required=True)

parser.add_argument('--out', '-o', help='Output file Name', default="translations.txt")

args=parser.parse_args()

textfile = open(args.input, 'r')
filetext = textfile.read()
textfile.close()
matches = re.findall('\{\{"[^"]*"\}\}', filetext)

translations = open(args.out, "w")
translations.write("# Only replace \"value\"s in this file\n")
for item in matches:
    translations.write("\nkey " + item[2:-2] + "\nvalue \"\"\n")

translations.close()
