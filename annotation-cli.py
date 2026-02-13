import csv
import os
import platform
import time
from datetime import datetime

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

    annotator_id = int(input("Enter the annotator ID: "))

    print("Are you working on the multiple annotator task? (y/n)")
    is_multiple_annotator_task = input().lower() == 'y'

    return annotator_id, annotators[annotator_id], is_multiple_annotator_task

def get_data(annotator_name):
    data = []
    with open(f'data-annotation/{annotator_name}/annotation_data.csv', 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def annotate_data(item, annotator_id):
    print(f"Text: {item['text']}")
    label = input("Enter the label for this text: ")
    item[f'a{annotator_id}'] = label
    return item

def write_annotated_data(item, current_datetime, writefile_path):
    # Get the current local date and time as a datetime object
    with open(f'{writefile_path}{current_datetime}.csv', 'a', encoding='utf-8') as f:
        f.write(f"{item['id']},{item['text']},{item['a0']},{item['a1']},{item['a2']},{item['a3']}\n")

def main():
    annotator_id, annotator_name, is_multiple_annotator_task = get_annotator()
    print(f"Annotator ID: {annotator_id}, Annotator Name: {annotator_name}")

    data_to_annotate = get_data(annotator_name)
    print(f'Are you ready to start annotating? (y/n)')
    ready = input().lower()

    if is_multiple_annotator_task:
        writefile_path = f'data-annotation/Multiple/sessions/'
    else:
        writefile_path = f'data-annotation/{annotator_name}/sessions/'

    if ready == 'y':
        # Create file & write header
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        with open(f'{writefile_path}{current_datetime}.csv', 'a', encoding='utf-8') as f:
                f.write(f"id,text,a0,a1,a2,a3\n")

        # Annotate each item and write to a separate file
        for item in data_to_annotate:
            clear_console()
            print()
            print()

            annotated_item = annotate_data(item, annotator_id)
            write_annotated_data(annotated_item, current_datetime, writefile_path)

        print("Annotation completed and saved successfully!")
        exit()
    else:
        print("Exiting the annotation CLI. Have a great day!")
        exit()

if __name__ == "__main__":
    main()