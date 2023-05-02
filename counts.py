import argparse
import os
import sys
import glob
from pathlib import Path
from collections import defaultdict

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

def get_counts(gender):
    directory = f"data_refined/{gender}"
    files = glob.glob(f"{directory}/*.txt")

    char_counts = defaultdict(int)
    line_counts = defaultdict(int)
    word_counts = defaultdict(int)
    
    # Sources: 
    # abhigoya. (2021). How to read multiple text files from folder in Python?. GeeksforGeeks. https://www.geeksforgeeks.org/how-to-read-multiple-text-files-from-folder-in-python/
    # cs95. (2019). How to extract the file name from a file path? [duplicate]. Stack Overflow. https://stackoverflow.com/questions/45113157/how-to-extract-the-file-name-from-a-file-path
    # W3Schools. (2023). Python String split() Method. https://www.w3schools.com/python/ref_string_split.asp#:~:text=The%20split()%20method%20splits,number%20of%20elements%20plus%20one
    for file in files:
        text = open(file, encoding='utf-8').read()
        cc = len(text)
        lc = len(text.split('\n'))
        wc = len(text.split())
        fname = os.path.basename(file)
        char_counts[fname] = cc
        line_counts[fname] = lc
        word_counts[fname] = wc

    return char_counts, line_counts, word_counts

def write_to_output(gender, char_counts, line_counts, word_counts):
    p = Path('results/')
    p.mkdir(parents=True, exist_ok=True)
    filepath = p / f'counts_{gender}.txt'
    with filepath.open("w+", encoding ="utf-8") as f:
        for title in sorted(char_counts):
            f.write(title + "\n")
            f.write("Character count: " + str(char_counts[title]) + "\n")
            f.write("Line count: " + str(line_counts[title]) + "\n")
            f.write("Word count: " + str(word_counts[title]) + "\n")
            f.write("\n")

def main():
    gender = get_args()
    char_counts, line_counts, word_counts = get_counts(gender)
    write_to_output(gender, char_counts, line_counts, word_counts)

if __name__ == "__main__":
    main()