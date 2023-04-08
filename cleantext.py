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
        text = text.partition('THE END.')[0]

        # set temp to be text in lowercase
        temp = text.lower()

        # find index where the text starts
        start_index = temp.find('chapter i.')
        if start_index == -1:
            start_index = temp.find('chapter 1.')
        if start_index != -1:
            text = text[start_index:]
            temp = temp[start_index:]
       
        # get all indices indicating end of volume
        volume_indices = []
        search_index = 0
        while True:
            i = temp.find('end of vol.', search_index)
            if i == -1:
                break
            volume_indices.append(i)
            search_index = i + 1
        
        # get rid of everything between end of volume and first chapter of the next volume
        for i in volume_indices:
            index = temp.find('chapter i.', i)
            if index == -1:
                index = temp.find('chapter 1.', i)
            if index != -1:
                text = text[:i] + text[index:]
                temp = temp[:i] + temp[index:]

        # final clean-up
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