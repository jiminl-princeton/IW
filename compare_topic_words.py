import sys
import argparse
import little_mallet_wrapper
import seaborn
import glob
from pathlib import Path
import nltk
from nltk.corpus import stopwords

def compare():
    words_female = set()
    path_female = f"results/female/mallet.topic_keys.5"
    with open(path_female, encoding='utf-8') as f:
        text = f.read()
        text = text.split("\n")
        text = text[:200]
        for line in text:
            info = line.split(":")
            words_female.add(info[2:])
    words_common = set()
    words_male = set()
    path_male = f"results/words_male.txt"
    with open(path_male, encoding='utf-8') as f:
        text = f.read()
        text = text.split("\n")
        for line in text:
            info = line.split()
            if word in words_female:
                words_common.add(word)
                words_female.remove(word)
            else:
                words_male.add(word)
    p = Path('results/')
    p.mkdir(parents=True, exist_ok=True)
    fname = f"words_common.txt"
    filepath = p / fname
    with filepath.open("w+", encoding ="utf-8") as f:
        for word in words_common:
            f.write(word + '\n')
    
    fname = f"words_unique_female.txt"
    filepath = p / fname
    with filepath.open("w+", encoding ="utf-8") as f:
        for word in words_female:
            f.write(word + '\n')

    fname = f"words_unique_male.txt"
    filepath = p / fname
    with filepath.open("w+", encoding ="utf-8") as f:
        for word in words_male:
            f.write(word + '\n')

def main():
    compare()

if __name__ == "__main__":
    main()