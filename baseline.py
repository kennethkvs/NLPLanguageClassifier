# create a baseline model which randomly predicts a label for each instance in the test set
import csv
import random

def baseline_predict(test_data, languages):
    predictions = []
    for item in test_data:
        label = random.choice(languages)
        predictions.append(label)
    return predictions

def gen_test_data(languages):
    # combine and mix the data from all test sets found in dataset/test/{lang}_test.csv
    # we want it to consist only of the text and the true label (language) for each instance
    test_data = []

    for lang in languages:
        path = f"dataset/test/{lang}_test.csv"
        with open(path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                test_data.append(row)

    random.shuffle(test_data)
    test_data = [{'text': item['text'], 'label': item['lang']} for item in test_data]
    return test_data

def evaluate(predictions, test_data):
    correct = 0
    total = len(test_data)

    for pred, item in zip(predictions, test_data):
        if pred == item['label']:
            correct += 1

    accuracy = correct / total if total > 0 else 0
    print(f"Baseline Accuracy: {accuracy:.2%} ({correct}/{total} correct predictions)")

def main():
    languages = ['af', 'de', 'en', 'es', 'fr', 'id', 'it', 'nl', 'pt', 'sv', 'tl', 'tr']
    test_data = gen_test_data(languages)

    predictions = baseline_predict(test_data, languages)
    # print("Predictions:", predictions[:10])  # Print the first 10 predictions for reference
    # print("Test data:", test_data[:10])  # Print the first 10 test data items for reference

    evaluate(predictions, test_data)

if __name__ == "__main__":
    main()


