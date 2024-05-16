#load the bug_report.json file and extract the image urls to dowlnoad
#mean time, automatically rename the image files and record file names in the json file field name image names for future reference

import json
import os
import requests
import shutil
# Load the JSON data
with open('data/bug_reports.json', 'r') as file:
    data = json.load(file)

index = 0
image_dir = 'data/images'

# Ensure the images directory exists
if not os.path.exists(image_dir):
    os.makedirs(image_dir)

# Process each row in the JSON data
for row in data:
    image_urls = row.get('image_urls', [])
    image_names = []
    
    for url in image_urls:
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()  # Check for HTTP errors
            image_name = f'{index}.png'
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
with open('data/bug_reports.json', 'w') as file:
    json.dump(data, file, indent=4)

print('All images downloaded and JSON file updated successfully.')
