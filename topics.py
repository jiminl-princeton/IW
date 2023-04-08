# Source: https://github.com/sceckert/IntroDHSpring2021/blob/main/_week9/introduction-to-topic-modeling.ipynb

import little_mallet_wrapper
import seaborn
import glob
from pathlib import Path

path_to_mallet = '~/Mallet-202108/bin/mallet'
directory = "data/1880smalecorpus"
files = glob.glob(f"{directory}/*.txt")

training_data = []
for file in files:
    text = open(file, encoding='utf-8').read()
    processed_text = little_mallet_wrapper.process_string(text, numbers='remove')
    training_data.append(processed_text)

original_texts = []
for file in files:
    text = open(file, encoding='utf-8').read()
    original_texts.append(text)

titles = [Path(file).stem for file in files]

#little_mallet_wrapper.print_dataset_stats(training_data)

num_topics = 15

output_directory_path = 'results'

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

# topics = little_mallet_wrapper.load_topic_keys(path_to_topic_keys)

# for topic_number, topic in enumerate(topics):
#     print(f"Topic {topic_number}\n\n{topic}\n")