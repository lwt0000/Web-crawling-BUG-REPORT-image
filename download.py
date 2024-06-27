import json
import os
import requests
import shutil
import glob

# Ensure the images directory exists
image_dir = 'data/images'
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# Function to download images and update JSON data
def download_images_and_update_json(json_file):
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    index = 0
    base_name = os.path.splitext(os.path.basename(json_file))[0].replace('\r', '').replace('\n', '')
    #locate the game name, the json file format is bug_reports_(game_name).json
    base_name = base_name[12:]
    print(f'base_name: {base_name}')
    for row in data:
        image_urls = row.get('image_urls', [])
        image_names = []

        # if image urls are empty, delete this row and update the json file
        if not image_urls:
            data.remove(row)
            continue
        for url in image_urls:
            try:
                response = requests.get(url, stream=True)
                response.raise_for_status()  # Check for HTTP errors
                image_name = f'{base_name}_{index}.png'
                image_path = os.path.join(image_dir, image_name)
                
                # Save the image to the specified directory
                with open(image_path, 'wb') as image_file:
                    shutil.copyfileobj(response.raw, image_file)
                
                image_names.append(image_name)
                print(f'{image_name} downloaded successfully')
                index += 1
            
            except requests.exceptions.RequestException as e:
                print(f'Error downloading {url}: {e}')
        
        # Update the JSON data with the new image names
        row['images_names'] = image_names
    
    # Save the modified JSON data back to the file
    with open(json_file, 'w', newline='') as file:
        json.dump(data, file, indent=4)

# Process each JSON file in the data directory
json_files = glob.glob('data/*.json')
for json_file in json_files:
    download_images_and_update_json(json_file)

print('All images downloaded and JSON files updated successfully.')



json_files = glob.glob('data/*.json')
row_removed = 0

for json_file in json_files:
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    original_length = len(data)
    data = [row for row in data if len(row['images_names']) != 0 and len(row['image_urls']) != 0]
    row_removed += original_length - len(data)
    
    with open(json_file, 'w', newline='') as file:
        json.dump(data, file, indent=4)

print(f'{row_removed} empty rows removed from JSON files.')