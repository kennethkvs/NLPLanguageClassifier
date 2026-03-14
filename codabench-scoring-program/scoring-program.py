import csv
import json
import os

from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, classification_report

# Path
input_dir = '/app/input'    # Input from ingestion program
output_dir = '/app/output/' # To write the scores
reference_dir = os.path.join(input_dir, 'ref')  # Ground truth data
prediction_dir = os.path.join(input_dir, 'res') # Prediction made by the model
score_file = os.path.join(output_dir, 'scores.json')          # Scores

def load_data(reference_dir, prediction_dir):
    # Load reference data
    ref_path = os.path.join(reference_dir, 'reference.csv')
    with open(ref_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        reference_data = [row for row in reader]

    # Load predictions
    pred_path = os.path.join(prediction_dir, 'prediction.csv')
    with open(pred_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        prediction_data = [row for row in reader]

    return reference_data, prediction_data

def evaluate(reference_data, prediction_data):
    reference_data.sort(key=lambda x: x['id'])
    prediction_data.sort(key=lambda x: x['id'])

    if len(reference_data) != len(prediction_data):
        raise ValueError("The number of predictions does not match the number of reference entries.")
    
    y_true = [item['lang'] for item in reference_data]
    y_pred = [item['lang'] for item in prediction_data]

    accuracy = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='macro')
    precision = precision_score(y_true, y_pred, average='macro')
    recall = recall_score(y_true, y_pred, average='macro')

    print(classification_report(y_true, y_pred))

    return accuracy, f1, precision, recall

def main():
    reference_data, prediction_data = load_data(reference_dir, prediction_dir)
    accuracy, f1, precision, recall = evaluate(reference_data, prediction_data)

    scores = {
        'accuracy': accuracy,
        'f1_score': f1,
        'precision': precision,
        'recall': recall
    }

    with open(score_file, 'w') as f:
        json.dump(scores, f)

if __name__ == "__main__":
    main()