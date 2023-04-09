import argparse
import os
import sys
import re
from collections import defaultdict
import glob
from pathlib import Path
import nltk
from nltk.corpus import stopwords
import string

def get_args():
    try:
        parser = argparse.ArgumentParser(allow_abbrev=False,
            description='Word frequency counter across all texts')
        parser.add_argument('gender', type=str, metavar='gender',
            help="gender of writers for corpus")
        parser.add_argument('unique', type=bool, metavar='unique',
            help="unique words only")
        args = parser.parse_args()
        gender = args.gender
        unique = args.unique
        if gender != "female" and gender != "male":
            print("Invalid gender of writers for corpus", file=sys.stderr)
            sys.exit(1)
        return gender, unique
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(2)

def get_word_freq(gender, unique=False):
    directory = f"data_refined/{gender}"
    files = glob.glob(f"{directory}/*.txt")
    word_freq = defaultdict(int)
    stop_words = set(stopwords.words('english'))
    stop_words.update(["would", "could", "wouldnt", "couldnt", "said"])

    if unique:
        for file in files:
            text = open(file, encoding='utf-8').read()
            text = text.lower()
            text = text.translate(str.maketrans('', '', string.punctuation.replace("-","")))
            words = nltk.word_tokenize(text)
            for word in words:
                if word not in stop_words:
                    word_freq[word] = word_freq.get(word, 0) + 1
    else:
        for file in files:
            text = open(file, encoding='utf-8').read()
            text = text.lower()
            words = nltk.word_tokenize(text)
            for word in words:
                word_freq[word] = word_freq.get(word, 0) + 1

    return word_freq

def write_to_output(gender, ordered_word_freq, unique=False):
    p = Path('results/')
    p.mkdir(parents=True, exist_ok=True)
    fname = f"wordfreq_{gender}"
    if unique:
        fname += "_unique"
    fname += ".txt"
    filepath = p / fname
    with filepath.open("w+", encoding ="utf-8") as f:
        for word in ordered_word_freq:
            f.write(word + ": " + str(ordered_word_freq[word]) + "\n")

def main():
    gender, unique = get_args()
    word_freq = get_word_freq(gender, unique)
    ordered_word_freq = dict(reversed(sorted(word_freq.items(), key=lambda x:x[1])))
    write_to_output(gender, ordered_word_freq, unique)

if __name__ == "__main__":
    main()