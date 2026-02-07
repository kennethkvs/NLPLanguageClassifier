from datasets import load_dataset


# English (en), Spanish (es), Italian (it), Afrikaans (af), Portuguese (pt), French (fr), Dutch (nl), German (de), Turkish (tr), Indonesian (id), Swedish (sv), and Tagalog (tl).
languages = ["en", "es", "it", "af", "pt", "fr", "nl", "de", "tr", "id", "sv", "tl"]
splits = ["train", "validation", "test"]

# Load the dataset
for language in languages:
    dataset = load_dataset("mteb/amazon_massive_scenario", language)
    
    for split in splits:
        num_rows = 5000 if split == "train" else dataset[split].num_rows
        # Access the specific split of the dataset
        split_data = dataset[split].shuffle(seed=42)[:num_rows]
        
        # Write the split data into a csv file
        with open(f"dataset/{split}/{language}_{split}.csv", "w", encoding="utf-8") as f:
            f.write("id,label,label_text,text,lang\n")
            for idx in range(num_rows):
                f.write(f"{split_data['id'][idx]},{split_data['label'][idx]},{split_data['label_text'][idx]},{split_data['text'][idx]},{split_data['lang'][idx]}\n")
