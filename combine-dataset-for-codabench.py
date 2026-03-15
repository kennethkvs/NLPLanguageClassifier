import random
import csv

languages = ['af', 'de', 'en', 'es', 'fr', 'id', 'it', 'nl', 'pt', 'sv', 'tl', 'tr']
splits = ['train', 'validation', 'test']

for split in splits:
    dataset = []
    for language in languages:
        data_path = f'dataset/{split}/{language}_{split}.csv'
        with open(data_path, 'r') as f:
          reader = csv.DictReader(f)
          for row in reader:
              dataset.append(row)
            
    random.seed(42)  # Set a seed for reproducibility
    random.shuffle(dataset)

    with open(f'codabench-starter-kit/dataset/{split}.csv', 'w') as writer:
        writer.write('id,text\n' if split == 'test' else 'id,text,lang\n')
        id_counter = 0
        for data in dataset:
            writer.writelines(f"{id_counter},{data['text']}\n" if split == 'test' else f"{id_counter},{data['text']},{data['lang']}\n")
            id_counter += 1

    if split == 'test':
        with open(f'codabench-reference-data/reference.csv', 'w') as writer:
            writer.write('id,lang\n')
            id_counter = 0
            for data in dataset:
                writer.writelines(f"{id_counter},{data['lang']}\n")
                id_counter += 1
            