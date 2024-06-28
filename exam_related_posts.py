import pandas as pd
import json

# Load the data
data = pd.read_csv('duplicates_images.csv')

related_post = []
count = 0
# Iterate through the data and skip the first two rows, extract the image and duplicates
for index, row in data.iterrows():
    if index < 2:
        continue

    image = row['image']
    duplicates = row['duplicates']
    duplicates = eval(duplicates)  # Convert the string to list

    # Extract the game name in the image path
    game_name = '_'.join(image.split('/')[2].split('_')[:-1])
    image_name = image.split('/')[-1]

    # Locate the game name JSON file
    game_json = f'data/bug_reports_{game_name}.json'
    related_pair = []
    # Load the JSON file
    with open(game_json, 'r') as file:
        bug_data = json.load(file)

        # Locate the image name in the JSON file
        for item in bug_data:
            image_names = item.get('images_names', [])
            if image_name in image_names:
                # Check if duplicates are in the image names
                for duplicate in duplicates:
                    duplicate_name = duplicate.split('/')[-1]
                    if duplicate_name in image_names:
                        # Found the duplicate from the same source, ignore
                        continue
                    else:
                        # We found an external duplicate, locate where it is from
                        # Combine this item with the external duplicate item and save it in a new JSON file
                        for bug in bug_data:
                            if duplicate_name in bug.get('images_names', []):
                                print(f'Found a related post for {image_name}')
                                # Found the external duplicate
                                external_duplicate = bug
                                # Combine the two items (combine dictionaries)
                                combined_data = {**item, **external_duplicate}
                                # Add to the related pair list
                                related_pair.append(combined_data)
                                #chekc if the combined data is already in the related post
                                if combined_data not in related_post:
                                    count += 1
                                    related_post.append(combined_data)
                                
                                

# Save the related post in a new JSON file
with open('data/related_post.json', 'w', newline='') as file:
    json.dump(related_post, file, indent=4)
print(f'{count} Related post saved successfully.')
print('Related post saved successfully.')
