# Script adapted from ocrfixer.py by Archie McKenzie
# Identifies all hapax legomena in a text, and asks Davinci if there is a better alternative

import sys
import os
import argparse
import glob
import openai

openai.api_key = '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'

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

def ocrfixer(gender):
    directory = f"data_refined/{gender}"
    # files = glob.glob(f"{directory}/*.txt")
    files = glob.glob(f"{directory}/AlexanderMrs__Monaschoiceanovel.txt")

    for file in files:
        # open the TXT file
        text = open(file, encoding='utf-8').read()

        # split the text into a list of sentences
        sentences = text.split('.')

        # create a dictionary to store the word counts
        word_counts = {}

        # iterate over each sentence in the list
        for sentence in sentences:
            # split the sentence into a list of words
            words = sentence.split()
            # iterate over each word in the list
            for word in words:
                # if the word is already in the dictionary, increment the count
                if word in word_counts:
                    word_counts[word] += 1
                # if the word is not in the dictionary, add it with a count of 1
                else:
                    word_counts[word] = 1

        # create a list to store words used only once
        unique_words = []
        unique_sentences = []

        # iterate over each word in the dictionary
        for word, count in word_counts.items():
            # if the word was used only once, add it to the list of unique words
            if count == 1:
                unique_words.append(word)

        # iterate over each sentence in the list
        for sentence in sentences:
            # check if the sentence contains a unique word
            contains_unique_word = False
            # split the sentence into a list of words
            words = sentence.split()
            # iterate over each word in the list
            for word in words:
                # if the word is in the list of unique words, mark the sentence as containing a unique word
                if word in unique_words:
                    contains_unique_word = True
                    break
            # if the sentence contains a unique word, print it
            if contains_unique_word:
                unique_sentences.append(sentence)

        print(unique_sentences)

        fixed_words = []

        i = 0
        for word in unique_words:
            prompt = 'The following sentence contains the unique word "' + word + '". If and only if that word is corrupted, mispelled, or out of context, return a single-word corrected replacement word. Otherwise return the single word unchanged. Sentence:\n\n' + unique_sentences[i]
            # generate text from the model
            response = openai.Completion.create(
                engine="text-davinci-003",
                prompt=prompt,
                temperature=0,
                max_tokens=50,
            )
            i += 1
            if (response.choices[0].text.strip() != word):
                fixed_words.append(response.choices[0].text.strip())
            else:
                fixed_words.append(word)

        # print the generated text
        print(fixed_words)

        # open the TXT file
        with open('original.txt', 'w') as f:
            for word in unique_words:
                f.write(word + '\n')

        # open the TXT file
        with open('corrected.txt', 'w') as f:
            for word in fixed_words:
                f.write(word + '\n')

def main():
    gender = get_args()
    fix_spelling(gender)

if __name__=="__main__":
    main()