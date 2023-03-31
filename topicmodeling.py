# Source: https://towardsdatascience.com/topic-modelling-in-python-with-nltk-and-gensim-4ef03213cd21

import argparse
import os
import sys
import spacy
from spacy.lang.en import English
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer

parser = English()
en_stop = set(nltk.corpus.stopwords.words('english'))
nlp = spacy.load("en_core_web_sm")

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

def tokenize(text):
    lda_tokens = []
    tokens = parser(text)
    for token in tokens:
        if token.orth_.isspace():
            continue
        elif token.like_url:
            lda_tokens.append('URL')
        elif token.orth_.startswith('@'):
            lda_tokens.append('SCREEN_NAME')
        else:
            lda_tokens.append(token.lower_)
    return lda_tokens

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma
    
def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

def prepare_text_for_lda(text):
    words = tokenize(text)
    words = [word for word in words if word not in en_stop]
    words = [get_lemma(word) for word in words]
    return words

def create_output_file(gender, all_topics):
    filepath = ""
    if gender == "female":
        filename = "topics_female.txt"
    elif gender == "male":
        filename = "topics_male.txt"
    new_path = "/Users/alicelee/Desktop/SPRING2023/IW/results/"
    with open(new_path + filename, "w+") as f:
        for topic in all_topics:
            for w in topic:
                f.write(w + " ")
            f.write("\n")
        nlp.max_length = 1006000

def main():
    root = "/Users/alicelee/Desktop/SPRING2023/IW"
    gender = get_args()
    path = get_path(gender)
    pwd = os.path.join(root, path)
    os.chdir(pwd)
    all_topics = []
    for file in sorted(os.listdir()):
        if file.endswith(".txt"):
            file_path = f"{pwd}/{file}"
            text = get_text(file_path)        
            words = prepare_text_for_lda(text)
            all_topics.append(words)

if __name__=="__main__":
    main()