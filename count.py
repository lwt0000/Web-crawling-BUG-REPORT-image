import os
import re

def extract_and_calculate_percentage(folder_path):
    # Define the pattern to search for
    pattern = re.compile(r'Answer#:\s*(Yes|No)', re.IGNORECASE)
    
    # Counters for 'Yes' and total answers
    yes_count = 0
    total_count = 0

    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                matches = pattern.findall(content)
                for match in matches:
                    total_count += 1
                    if match.lower() == 'yes':
                        yes_count += 1

    # Calculate the percentage of 'Yes' answers
    if total_count > 0:
        yes_percentage = (yes_count / total_count) * 100
    else:
        yes_percentage = 0

    # Print the results
    print(f"Total Answers: {total_count}")
    print(f"'Yes' Answers: {yes_count}")
    print(f"Percentage of 'Yes' Answers: {yes_percentage:.2f}%")

# Example usage
folder_path = 'ollama_data'
extract_and_calculate_percentage(folder_path)
