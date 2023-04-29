# Source: https://github.com/sceckert/IntroDHSpring2021/blob/main/_week9/introduction-to-topic-modeling.ipynb

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

def get_topics(gender):
    path_to_mallet = '~/Mallet-202108/bin/mallet'
    sample_path = f"results/{gender}_subset_titles.txt"
    sample = []
    with open(sample_path, encoding='utf-8') as f:
        text = f.read()
        sample = text.split("\n")
        sample = sample[:len(sample) - 1]
    files = []
    for s in sample:
        files.append(f"data_refined/{gender}/" + s + ".txt")
    training_data = []

    stop_words = set(stopwords.words('english'))
    stop_words.update(["would", "could", "said", "illinois"])
    stop_words = list(stop_words)
    
    for file in files:
        with open(file, encoding='utf-8') as f:
            text = f.read()
            processed_text = little_mallet_wrapper.process_string(text, numbers='remove', stop_words=stop_words)
            training_data.append(processed_text)

    original_texts = []
    for file in files:
        with open(file, encoding='utf-8') as f:
            text = f.read()
            original_texts.append(text)

    titles = [Path(file).stem for file in files]

    little_mallet_wrapper.print_dataset_stats(training_data)

    num_topics = 25

    output_directory_path = f'results/{gender}_subset'

    Path(f"{output_directory_path}").mkdir(parents=True, exist_ok=True)

    path_to_training_data           = f"{output_directory_path}/training.txt"
    path_to_formatted_training_data = f"{output_directory_path}/mallet.training"
    path_to_model                   = f"{output_directory_path}/mallet.model.{str(num_topics)}"
    path_to_topic_keys              = f"{output_directory_path}/mallet.topic_keys.{str(num_topics)}"
    path_to_topic_distributions     = f"{output_directory_path}/mallet.topic_distributions.{str(num_topics)}"
    path_to_word_weights	        = f"{output_directory_path}/mallet.topic_weights.{str(num_topics)}"
    path_to_word_diagnostics        = f"{output_directory_path}/mallet.topic_diagnostics.{str(num_topics)}"


    little_mallet_wrapper.import_data(path_to_mallet,
                    path_to_training_data,
                    path_to_formatted_training_data,
                    training_data)

    little_mallet_wrapper.train_topic_model(path_to_mallet,
                        path_to_formatted_training_data,
                        path_to_model,
                        path_to_topic_keys,
                        path_to_topic_distributions,
                        path_to_word_weights,
                        path_to_word_diagnostics,
                        num_topics)

    topics = little_mallet_wrapper.load_topic_keys(path_to_topic_keys)

    for topic_number, topic in enumerate(topics):
        print(f"Topic {topic_number}\n\n{topic}\n")

def main():
    gender = get_args()
    get_topics(gender)

if __name__ == "__main__":
    main()