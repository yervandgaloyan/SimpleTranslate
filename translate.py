#!/usr/bin/env python3
import argparse


parser=argparse.ArgumentParser(
    description='Simple Translate. Created by Yervand Galoyan', 
    )

requiredNamed = parser.add_argument_group('required named arguments')
requiredNamed.add_argument('--input', '-i', help='Input file name', required=True)
requiredNamed.add_argument('--translation', '-t', help='Input translation file name', required=True)

parser.add_argument('--out', '-o', help='Output file Name')

args=parser.parse_args()

print(args.out)

if args.out is None:    
    args.out = args.input

dictionary = {}

translations = open(args.translation, 'r')
translationsLines = translations.readlines()

translations.close()

# print(translationsLines)

for item in range(2,len(translationsLines),3):
    dictionary[translationsLines[item][5:-2]] = translationsLines[item+1][7:-2]

# print(dictionary)

textfile = open(args.input, 'r')
fileData = textfile.read()
textfile.close()


for item in dictionary:
    fileData = fileData.replace("{{\"" + item + "\"}}", dictionary[item])

with open(args.out, 'w') as outputFile:
  outputFile.write(fileData)