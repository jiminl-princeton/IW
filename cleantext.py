import sys
import os
import argparse
import glob
from pathlib import Path

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

def clean_text(gender):
    directory = f"data/1880s{gender}corpus"
    files = glob.glob(f"{directory}/*.txt")

    for file in files:
        text = open(file, encoding='utf-8').read()

        # delete everything after the end
        end = text.find('THE END.')
        if end == -1:
            end = text.find('THE EN1>')
        if end != -1:
            text = text[:end]

        # set temp to be text in lowercase
        temp = text.lower()

        # find index where the text starts
        start = text.find('PROLOGUE.')
        start_words = ['chapte', 'chapter i.', 'chapter 1.']
        t = float('inf')
        if start == -1:
            for start_word in start_words:
                if temp.find(start_word) != -1:
                    t = min(t, temp.find(start_word))
            if t != float('inf') and t != -1:
                start = t
        if start != -1:
            text = text[start:]
            temp = temp[start:]

        # get all indices indicating end of volume
        search_index = 0
        end_words = ['END OF ', 'End OF ', 'END OP ', 'ED OF VOL']
        while True:
            i = temp.find('end of vol', search_index)
            t = float('inf')
            for end_word in end_words:
                if text.find(end_word, search_index) != -1:
                    t = min(t, text.find(end_word, search_index))
            if i == -1 and (t == -1 or t == float('inf')):
                break
            i = min(i, t)
            search_index = i + 1
            n = temp.find('chapter', search_index)
            if n != -1:
                text = text[:i] + text[n:]
                temp = temp[:i] + temp[n:]
        
        # remove occurrences of "library" and "university of illinois" from ocr scans
        text = text.replace("LIBRARY", "")
        text = text.replace("UNIVERSITY OF ILLINOIS", "")
        text = text.replace("UNIVERSITY OF", "")
        text = text.replace("ILLINOIS", "")

        # final clean-up, remove 
        text = "".join([x if ord(x) < 128 and x != '^' else '' for x in text])

        # write to output path
        p1 = Path('data_refined/')
        p1.mkdir(parents=True, exist_ok=True)
        p2 = Path(f'data_refined/{gender}/')
        p2.mkdir(parents=True, exist_ok=True)
        fname = os.path.basename(file)
        filepath = p2 / fname
        with filepath.open("w+", encoding ="utf-8") as f:
            f.write(text)

def main():
    gender = get_args()
    clean_text(gender)

if __name__=="__main__":
    main()