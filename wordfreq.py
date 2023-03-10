import argparse
import os
import sys
from collections import defaultdict

word_freq = defaultdict(int)

def get_args():
    try:
        parser = argparse.ArgumentParser(allow_abbrev=False,
            description='Word frequency counter across all texts')
        parser.add_argument('path', type=str, metavar='path',
            help="path to data")
        args = parser.parse_args()
        path = args.path
        return path
    except Exception as ex:
        print(ex, file=sys.stderr)
        sys.exit(2)

def read_text_file(file_path):
    words = []
    with open(file_path, 'r') as f:
        txt = f.read()
        words = txt.split()
    for word in words:
        word_freq[word] = word_freq.get(word, 0) + 1

def get_words(path):
    root = "/Users/alicelee/Desktop/IW"
    pwd = os.path.join(root, path)
    os.chdir(pwd)
    for file in sorted(os.listdir()):
        if file.endswith(".txt"):
            file_path = f"{pwd}/{file}"
            fname = os.path.basename(file)
            read_text_file(file_path)
    ordered_word_freq = dict(sorted(word_freq.items(), key=lambda x:x[1]))
    res = {}
    for w in ordered_word_freq:
        res[w] = res.get(w, 0) + 1
    return res

def main():
    root = "/Users/alicelee/Desktop/SPRING2023/IW"
    path = get_args()
    pwd = os.path.join(root, path)
    os.chdir(pwd)
    for file in sorted(os.listdir()):
        if file.endswith(".txt"):
            file_path = f"{pwd}/{file}"
            fname = os.path.basename(file)
            read_text_file(file_path)
    ordered_word_freq = dict(sorted(word_freq.items(), key=lambda x:x[1]))
    filename = ""
    if path == "data/1880sfemalecorpus":
        filename = "wordfreq_female.txt"
    elif path == "data/1880smalecorpus":
        filename = "wordfreq_male.txt"
    new_path = "/Users/alicelee/Desktop/SPRING2023/IW/results/"
    with open(new_path + filename, "w+") as f:
        for w in ordered_word_freq:
            f.write(w + ": " + str(ordered_word_freq[w]) + "\n")
    # for w in ordered_word_freq:
    #     print(w + ":", ordered_word_freq[w])

if __name__ == "__main__":
    main()