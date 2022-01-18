# SimpleTranslate
Simple translation script.


Add in your file that you want to translate keywords like {{"YOUR KEYWORD HERE"}}

git clone https://github.com/yervandgaloyan/SimpleTranslate.git

python3 getKeys.py -i "YOUR FILE NAME TO PARSE" -o "TRANSLATIONS FILE NAME"

Change values in "TRANSLATIONS FILE NAME"

python3 translate.py -i "YOUR FILE NAME TO TRANSLATE" -t "TRANSLATIONS FILE NAME" -o "OUTPUT FILE NAME"


<!-- TODO Add translations file check -->
<!-- TODO Add complete README.md file -->