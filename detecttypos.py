import argparse
import os
import sys
import glob
from pathlib import Path
from spellchecker import SpellChecker
import string

def get_args():
    try:
        parser = argparse.ArgumentParser(allow_abbrev=False,
            description='Word frequency counter across all texts')
        parser.add_argument('gender', type=str, metavar='gender',
            help="gender of writers for corpus")
        args = parser.parse_args()
        gender = args.gender
        if gender != "female" and gender != "male":
            print("Invalid gender of writers for corpus", file=sys.stderr)
            sys.exit(1)
        return gender
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(2)

def get_misspelled_words(gender):
    spell = SpellChecker()
    directory = f"data_refined/{gender}"
    files = glob.glob(f"{directory}/*.txt")
    misspelled_words = []
    for file in files:
        text = open(file, encoding='utf-8').read()
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation.replace("-","")))
        text = text.split()
        misspelled_words += spell.unknown(text)
    return misspelled_words

def write_to_output(gender, misspelled_words):
    p = Path('results/')
    p.mkdir(parents=True, exist_ok=True)
    filepath = p / f'misspelled_{gender}.txt'
    with filepath.open("w+", encoding ="utf-8") as f:
        for word in sorted(misspelled_words):
            f.write(word)
            f.write("\n")

def main():
    gender = get_args()
    misspelled_words = get_misspelled_words(gender)
    misspelled_words = set(misspelled_words)
    write_to_output(gender, misspelled_words)

if __name__ == "__main__":
    main()