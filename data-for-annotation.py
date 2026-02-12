import csv
import random

languages = ["en", "es", "it", "af", "pt", "fr", "nl", "de", "tr", "id", "sv", "tl"]
annotators = {0:'Elite', 1:'Ishpreet', 2:'Kenneth', 3:'Tania', 4:'Multiple'}

data = {}
for language in languages:
    data[language] = []
    # Retrieve all the data files for the language
    with open(f'dataset/train/{language}_train.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data[language].append(f'{row["id"]},{row["text"]}')

for annotator_id, annotator_name in annotators.items():
    with open(f'data-annotation/{annotator_name}/annotation_data.csv', 'w', encoding='utf-8') as f:
        f.write("id,text,a0,a1,a2,a3,a4\n")
        all_data = []

        # For each language, get the corresponding data for the annotator
        for language in languages:
            all_data.append(data[language][annotator_id*100:(annotator_id+1)*100])
        all_data = [item for sublist in all_data for item in sublist]  # Flatten the list
        random.seed(42)  # Set a seed for reproducibility
        random.shuffle(all_data)  # Shuffle the data

        # Write the data into the csv file
        for item in all_data:
            f.write(f"{item},,,,,\n")