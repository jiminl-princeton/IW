from textblob import TextBlob
from spellchecker import SpellChecker
import wordfreq

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

def main():
    root = "/Users/alicelee/Desktop/IW"
    path = get_args()
    spell = SpellChecker()
    word_freq = wordfreq.get_words(path)