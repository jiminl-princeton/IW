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
    # files = glob.glob(f"{directory}/PriceEleanorCEleanorCatherine__Redtowers.txt")
    # files = glob.glob(f"{directory}/AlexanderMrs__Monaschoiceanovel.txt")
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
        start = float('inf')
        found = False
        search_index = 0
        prologue = ""
        start_words = ['PROLOGUE', 'Prologue']
        for start_word in start_words:
            if text.find(start_word) != -1:
                start = min(start, text.find(start_word))
                if start == text.find(start_word):
                    prologue = start_word
                    search_index = start + 1
                found = True
        if found:
            while True:
                i = text.find(prologue, search_index)
                if i == -1:
                    break
                start = i
                search_index = i + 1
        if not found:
            start_words = ['chapter i.', 'chapter 1.', 'chaptee i.', 'chaptee 1.', 'hapter i.', 'hapter 1.', 'chapter i\n', 'chapter 1\n']
            for start_word in start_words:
                if temp.find(start_word) != -1:
                    start = min(start, temp.find(start_word))
                    found = True
        if not found:
            if text.find('CONTENT') != -1:
                start = text.find('CONTENT')
                found = True
        # if not found:
        #     start_words = ['CHAPTEE', 'CHAPT', 'CHAPTER', 'CHAP.', 'Chapter']
        #     for start_word in start_words:
        #         if text.find(start_word) != -1:
        #             start = min(start, text.find(start_word))
        #             found = True
        if found:
            text = text[start:]
            temp = temp[start:]
       
        # get all indices indicating end of volume
        search_index = 0
        end_words = ['END OP VOL', 'ED OF VOL']
        next_words = ['CHAPTER ', 'CHAPTER\n']
        next_words_ = ['chapter i.', 'chapter 1.', 'chaptee i.', 'chaptee 1.', 'hapter i.', 'hapter 1.', 'chapter i\n', 'chapter 1\n']

        while True:
            i = float('inf')
            found = False
            if temp.find('end of vol', search_index) != -1:
                i = temp.find('end of vol', search_index)
                found = True
            if not found:
                for end_word in end_words:
                    if text.find(end_word, search_index) != -1:
                        i = min(i, text.find(end_word, search_index))
                        found = True
            if not found:
                break
            search_index = i + 1
            n = float('inf')
            found = False
            # for next_word in next_words_:
            #     if temp.find(next_word) != -1:
            #         n = min(n, temp.find(next_word, search_index))
            #         print(temp.find(next_word, search_index), search_index)
            #         found = True
            if not found:
                for next_word in next_words:
                    if text.find(next_word, search_index) != -1:
                        n = min(n, text.find(next_word, search_index))
                        found = True
            if found:
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