import sys
import argparse
import little_mallet_wrapper
import seaborn
import glob
from pathlib import Path
import nltk
from nltk.corpus import stopwords
import random

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

def get_authors(gender):
    directory = f"data_refined/{gender}"
    files = glob.glob(f"{directory}/*.txt")
    titles = [Path(file).stem for file in files]
    
    authors = {}
    for title in titles:
        i = title.find('_')
        author = title[:i]
        authors[author] = authors.get(author, 0) + 1
    ordered_authors = dict(reversed(sorted(authors.items(), key=lambda x:x[1])))

    p = Path('results/')
    p.mkdir(parents=True, exist_ok=True)
    fname = f"authors_{gender}"
    fname += ".txt"
    filepath = p / fname
    with filepath.open("w+", encoding ="utf-8") as f:
        for author in ordered_authors:
            f.write(author + ": " + str(ordered_authors[author]) + "\n")

def main():
    gender = get_args()
    get_authors(gender)

if __name__ == "__main__":
    main()