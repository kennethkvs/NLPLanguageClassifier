import csv
import os
import platform
from datetime import datetime

languages = {
    "en": "English", 
    "es": "Spanish", 
    "it": "Italian", 
    "af": "Afrikaans", 
    "pt": "Portuguese", 
    "fr": "French", 
    "nl": "Dutch", 
    "de": "German", 
    "tr": "Turkish", 
    "id": "Indonesian", 
    "sv": "Swedish", 
    "tl": "Tagalog"
}
annotators = {0:'Elite', 1:'Ishpreet', 2:'Kenneth', 3:'Tania'}

def clear_console():
    """
    Clears the console screen across different operating systems.
    """
    # Check the operating system name
    if platform.system() == "Windows":
        # For Windows, use 'cls' command
        os.system('cls')
    else:
        # For Linux/macOS (posix), use 'clear' command
        os.system('clear')

def get_annotator():
    print(
    '''
    Welcome to the annotation CLI!

    Please select an annotator from the following List (0-3):
    0: Elite
    1: Ishpreet
    2: Kenneth
    3: Tania
    ''')

    while True:
        annotator_id = int(input("Enter the annotator ID: "))
        if annotator_id in range(4):
            break
        else:
            print("Invalid annotator ID. Please enter a valid ID from the list.")

    while True:
        is_multiple_annotator_task = input("Are you working on the multiple annotator task? (y/n) ").lower()
        if is_multiple_annotator_task in ['y', 'n']:
            is_multiple_annotator_task = (is_multiple_annotator_task == 'y')
            break
        else:
            print("Invalid value. Please enter 'y' for yes or 'n' for no.")

    return annotator_id, annotators[annotator_id], is_multiple_annotator_task

def get_data(base_path):
    data = []
    with open(f'{base_path}/annotation_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def annotate_data(item, annotator_id):
    print(f'''
    Type 's' or 'stop' to end the annotation session. 

    Please read the following text and provide a label for it based on the language it is written in.
        
    The possible labels are (label: language):
    en: English          af: Afrikaans          nl: Dutch              id: Indonesian
    es: Spanish          pt: Portuguese         de: German             sv: Swedish
    it: Italian          fr: French             tr: Turkish            tl: Tagalog

    Text: {item['text']}\n
    ''')

    while True:
        label = input("Enter the label for this text: ")
        if label.lower() in ['s', 'stop']:
            return item, True
        if label in languages:
            item[f'a{annotator_id}'] = label
            return item, False
        else:
            print("Invalid label. Please enter a valid label from the list.")

def write_annotated_data(item, current_datetime, base_path):
    # Get the current local date and time as a datetime object
    with open(f'{base_path}/sessions/{current_datetime}.csv', 'a', encoding='utf-8') as f:
        f.write(f"{item['id']},{item['text']},{item['a0']},{item['a1']},{item['a2']},{item['a3']}\n")

def save_session_data(base_path, current_datetime, initial_data):
    with open(f'{base_path}/sessions/{current_datetime}.csv', 'r', encoding='utf-8') as session_file:
        reader = csv.DictReader(session_file)
        annotated_data = list(reader)
        with open(f'{base_path}/annotation_data.csv', 'w', encoding='utf-8') as original_file:
            fieldnames = ['id', 'text', 'a0', 'a1', 'a2', 'a3']
            writer = csv.DictWriter(original_file, fieldnames=fieldnames)
            writer.writeheader()
            for item in initial_data:
                for annotated_item in annotated_data:
                    if item['id'] == annotated_item['id']:
                        item.update(annotated_item)
                writer.writerow(item)

def main():
    annotator_id, annotator_name, is_multiple_annotator_task = get_annotator()
    print(f"Annotator ID: {annotator_id}, Annotator Name: {annotator_name}, Multiple Annotator Task: {is_multiple_annotator_task}\n")  

    if is_multiple_annotator_task:
        base_path = f'data-annotation/Multiple'
    else:
        base_path = f'data-annotation/{annotator_name}'

    data_to_annotate = get_data(base_path)
    while True:
        ready = input('Are you ready to start annotating? (y/n) ').lower()
        if ready in ['y', 'n']:
            break
        else:
            print("Invalid value. Please enter 'y' for yes or 'n' for no.")

    if ready == 'y':
        # Create file & write header
        data_annotated_counter = 0
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        with open(f'{base_path}/sessions/{current_datetime}.csv', 'a', encoding='utf-8') as f:
            f.write(f"id,text,a0,a1,a2,a3\n")

        # Annotate each item and write to a separate file
        for item in data_to_annotate:
            if item[f'a{annotator_id}'] != '':
                data_annotated_counter += 1
                continue

            clear_console()
            print('\n\n') # Add an extra line break for better readability in the console

            print(f'Annotated {data_annotated_counter} out of {len(data_to_annotate)} items.\n')
            annotated_item, is_stopping = annotate_data(item, annotator_id)

            if is_stopping:
                print("Stopping the annotation session...")
                save_session_data(base_path, current_datetime, data_to_annotate)

                print("Session data saved successfully!")
                exit()
            else:
                write_annotated_data(annotated_item, current_datetime, base_path)
                data_annotated_counter += 1

        print("Annotation session completed for all items. Saving the session data...")
        save_session_data(base_path, current_datetime, data_to_annotate)

        print("Annotation completed and saved successfully!")
        exit()
    else:
        print("Exiting the annotation CLI. Have a great day!")
        exit()

if __name__ == "__main__":
    main()