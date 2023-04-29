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

def get_sample(gender):
    directory = f"data_refined/{gender}"
    files = glob.glob(f"{directory}/*.txt")
    files = get_sample(gender, files)
    titles = [Path(file).stem for file in files]
    sample = random.sample(titles, int(0.8 * len(titles)))
    p = Path('results/')
    p.mkdir(parents=True, exist_ok=True)
    fname = f"subset_titles_{gender}"
    fname += ".txt"
    filepath = p / fname
    with filepath.open("w+", encoding ="utf-8") as f:
        for s in sample:
            f.write(s + '\n')

def main():
    gender = get_args()
    get_sample(gender)

if __name__ == "__main__":
    main()