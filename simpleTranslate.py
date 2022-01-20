#!/usr/bin/env python3
import argparse
from configparser import ConfigParser
import glob
from pathlib import Path
import re


parser=argparse.ArgumentParser(
    description='Simple Translate.', 
    )

requiredNamed = parser.add_argument_group('Get Configurations')
requiredNamed.add_argument('--getConf', '-gc', help='Get Configurations', action='store_true')

requiredNamed = parser.add_argument_group('Set Configurations')

requiredNamed.add_argument('--setConf', '-sc', help='Set Configurations', action='store_true')
requiredNamed.add_argument('--inputFile', '-if', help='Input file name')
requiredNamed.add_argument('--translationFolder', '-tf', help='Input translation folder name')
requiredNamed.add_argument('--buildFolder', '-bf', help='Build folder name')

requiredNamed = parser.add_argument_group('Get Translation Keys')
requiredNamed.add_argument('--getKeys', '-gk', help='Get Translation Keys', action='store_true')

requiredNamed = parser.add_argument_group('Build')
requiredNamed.add_argument('--build', '-b', help='Build translations', action='store_true')
args=parser.parse_args()


config = ConfigParser()
config.read('translationConfigs.ini')

if args.getConf:
    if not config.has_section('main'):
        print('\033[1;37;41mConfigurations not exists.\033[0;0m')
        exit()
        
    if config.has_option('main', 'inputFile'):
        print('Input File : \033[1;32m' + config.get('main', 'inputFile') + '\033[0;0m')
    else:
        print('Input File : \033[1;31mNone\033[0;0m')

    if config.has_option('main', 'translationsFolder'):
        print('Translations Folder : \033[1;32m' + config.get('main', 'translationsFolder') + '\033[0;0m')
    else:
        print('Translations Folder : \033[1;31mNone\033[0;0m')

    if config.has_option('main', 'buildFolder'):
        print('Build Folder : \033[1;32m' + config.get('main', 'buildFolder') + '\033[0;0m')
    else:
        print('Build Folder : \033[1;31mNone\033[0;0m')


if args.setConf:
    if not config.has_section('main'):
        config.add_section('main')
    if args.inputFile:
        config.set('main', 'inputFile', args.inputFile)
    if args.translationFolder:
        config.set('main', 'translationsFolder', args.translationFolder)
    if args.buildFolder:
        config.set('main', 'buildFolder', args.buildFolder)
    
    with open('translationConfigs.ini', 'w') as f:
        config.write(f)

if args.getKeys:
    if not config.has_option('main', 'inputFile'):
        print('\033[1;31mInput File not given, please set input file in configurations\033[0;0m')
        exit()
    
    textfile = open(config.get('main', 'inputFile'), 'r')
    filetext = textfile.read()
    textfile.close()
    matches = re.findall('\{\{"[^"]*"\}\}', filetext)

    matches = set(matches)
    
    if not config.has_option('main', 'translationsFolder'):
        dir = Path('translations/')
        dir.mkdir(parents=True, exist_ok=True)
    else:
        dir = Path(config.get('main', 'translationsFolder'))
        dir.mkdir(parents=True, exist_ok=True)
    
    filename = Path(str(dir) + '/translations.txt')
    filename.touch(exist_ok=True) 
    
    with open(filename, 'w') as translations:
        translations.write("# Only replace \"value\"s in this file \n")
        translations.write("\nkey \"lang\"\nvalue \"\"\n")
        for item in matches:
            translations.write("\nkey " + item[2:-2] + "\nvalue \"\"\n")

if args.build:
    if not config.has_option('main', 'translationsFolder'):
        dir = 'translations'
    else:
        dir = config.get('main', 'translationsFolder')

    dictionary = {}

    for tr in glob.glob(dir + "/*.txt"):
        translations = open(tr, 'r')
        translationsLines = translations.readlines()

        translations.close()

        # print(translationsLines)

        for item in range(2,len(translationsLines),3):
            dictionary[translationsLines[item][5:-2]] = translationsLines[item+1][7:-2]

        # print(dictionary)
        if not config.has_option('main', 'inputFile'):
            print('\033[1;31mInput File not given, please set input file in configurations\033[0;0m')
            exit()
    
        textfile = open(config.get('main', 'inputFile'), 'r')
        fileData = textfile.read()
        textfile.close()


        for item in dictionary:
            fileData = fileData.replace("{{\"" + item + "\"}}", dictionary[item])

        if not config.has_option('main', 'buildFolder'):
                dir = Path('builds/')
                dir.mkdir(parents=True, exist_ok=True)
        else:
            dir = Path(config.get('main', 'buildFolder'))
            dir.mkdir(parents=True, exist_ok=True)
        
        # print(dictionary)
        filename = Path(str(dir) + "/" + dictionary["lang"] + config.get('main', 'inputFile'))
        filename.touch(exist_ok=True) 

        with open(filename, 'w') as outputFile:
            outputFile.write(fileData)