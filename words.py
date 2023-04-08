import argparse
import os
import sys
from collections import defaultdict
import re
import nltk

word_freq = defaultdict(int)

def get_args():
    try:
        parser = argparse.ArgumentParser(allow_abbrev=False,
            description='Word frequency counter across all texts')
        parser.add_argument('gender', type=str, metavar='gender',
            help="gender of writers for corpus")
        args = parser.parse_args()
        gender = args.gender
        return gender
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(2)

def get_path(gender):
    path = ""
    if gender == "female":
        path = "data/1880sfemalecorpus"
    elif gender == "male":
        path = "data/1880smalecorpus"
    else:
        print("Invalid gender of writers for corpus", file=sys.stderr)
        sys.exit(1)
    return path

def get_text(file_path):
    with open(file_path, 'r') as f:
        text = f.read()
        # Source: https://stackoverflow.com/questions/1342000/how-to-make-the-python-interpreter-correctly-handle-non-ascii-characters-in-stri
        text = "".join([x if ord(x) < 128 and x != '^' else '' for x in text])
    return text

def update_word_freq(text):
    tokenlist = nltk.word_tokenize(text)
    for token in tokenlist:
        word_freq[token] = word_freq.get(token, 0) + 1

def create_output_file(gender, ordered_word_freq):
    filename = ""
    if gender == "female":
        filename = "wordfreq_female.txt"
    elif gender == "male":
        filename = "wordfreq_male.txt"
    new_path = "/Users/alicelee/Desktop/SPRING2023/IW/results/"
    with open(new_path + filename, "w+") as f:
        for w in ordered_word_freq:
            f.write(w + ": " + str(ordered_word_freq[w]) + "\n")

def main():
    root = "/Users/alicelee/Desktop/SPRING2023/IW"
    gender = get_args()
    path = get_path(gender)
    pwd = os.path.join(root, path)
    os.chdir(pwd)
    for file in sorted(os.listdir()):
        if file.endswith(".txt"):
            file_path = f"{pwd}/{file}"
            text = get_text(file_path)
            update_word_freq(text)
    ordered_word_freq = dict(reversed(sorted(word_freq.items(), key=lambda x:x[1])))
    create_output_file(gender, ordered_word_freq)

if __name__ == "__main__":
    main()