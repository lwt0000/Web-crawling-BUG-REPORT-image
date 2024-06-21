import requests
import json
import base64
import os
import random
import glob
sample_size = 96
path = os.getcwd() + "Web-crawling-BUG-REPORT-image/data/images"
data_path = os.getcwd() + "Web-crawling-BUG-REPORT-image/data"
images_path = "data/images/"
ollama_data_path ="ollama_data"
os.makedirs(ollama_data_path, exist_ok=True)


url = "http://localhost:19999/api/generate"

def sample_data_QA(json_file):
    # load the json file
    with open(json_file, 'r') as file:
        data = json.load(file)
    
    #randomly select sample_size number of rows
    # if sample_size is greater than the total number of rows, set sample_size to the total number of rows
    if sample_size > len(data):
        sample_size = len(data)
    random_rows = random.sample(data, sample_size)
    #for each row extract images names and descriptions
    for i, row in enumerate(random_rows):
        image_names = row.get('images_names', [])
        descriptions = row.get('description')
        for each in image_names:
            #load the image
           
            image_path = images_path + each
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            # URL for the Ollama server

           
            # Input data (e.g., a text prompt)
            question = descriptions + " \n The image provided to you is a user reported buggy image, do you think it matches the above description? Please provide your answer begins with either 'Yes' or 'No,' followed by a detail explanation."
            data = {
                "model": "llava:34b",
                "prompt": question,
                "images": [encoded_string]
            }

            # Make a POST request to the server
            response = requests.post(url, json=data)
            # Check if the request was successful
            if response.status_code == 200:
                # Process the response
                response_text = response.text

                # Convert each line to json
                response_lines = response_text.splitlines()
                response_json = [json.loads(line) for line in response_lines]
                text = ""
                for line in response_json:
                    # Print the response. No line break
                    # print(line['response'], end="")
                    text += line['response']
                output = text
            else:
                print("Error:", response.status_code)

            save_path = os.path.join(ollama_data_path, f"llava_34b_{i}_{each}.txt")
            with open(save_path, "w") as fw:
                
                ans = "Answer#"+": "+ output + "\n"
                fw.write(ans)
            print(f"image {i+1}/{sample_size} completed")
                






json_files = glob.glob('data/*.json')
for json_file in json_files:
    sample_data_QA(json_file)





