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
        args = parser.parse_args()
        gender = args.gender
        if gender != "female" and gender != "male":
            print("Invalid gender of writers for corpus", file=sys.stderr)
            sys.exit(1)
        return gender
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(2)

def get_word_freq(gender, unique=False):
    directory = f"data_refined/{gender}"
    files = glob.glob(f"{directory}/*.txt")
    word_freq = defaultdict(int)
    # misspelled_words_file = f"results/misspelled_{gender}.txt"
    # misspelled_words = []
    # with open(misspelled_words_file, encoding='utf-8') as f:
    #     text = f.read()
    #     misspelled_words = text.split()
    stop_words = set(stopwords.words('english'))
    stop_words.update(["said"])

    for file in files:
        text = open(file, encoding='utf-8').read()
        text = ''.join([i for i in text if not i.isdigit()])
        text = text.lower()
        text = text.translate(str.maketrans('', '', string.punctuation.replace("-","")))
        words = nltk.word_tokenize(text)
        for word in words:
            if word not in stop_words:
                word_freq[word] = word_freq.get(word, 0) + 1

    return word_freq

def write_to_output(gender, ordered_word_freq):
    p = Path('results/')
    p.mkdir(parents=True, exist_ok=True)
    fname = f"wordfreq_{gender}"
    fname += ".txt"
    filepath = p / fname
    with filepath.open("w+", encoding ="utf-8") as f:
        for word in ordered_word_freq:
            f.write(word + ": " + str(ordered_word_freq[word]) + "\n")

def main():
    gender = get_args()
    word_freq = get_word_freq(gender)
    ordered_word_freq = dict(reversed(sorted(word_freq.items(), key=lambda x:x[1])))
    write_to_output(gender, ordered_word_freq)

if __name__ == "__main__":
    main()