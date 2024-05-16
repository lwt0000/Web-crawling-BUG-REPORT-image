import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin
# url = 'https://answers.ea.com/t5/Bug-Reports/Textures-Medium-and-below-are-very-blurry-in-all-Menus/td-p/13698266?attachment-id=816308'
url = 'https://answers.ea.com/t5/Bug-Reports/Textures-Medium-and-below-are-very-blurry-in-all-Menus/td-p/13698266'
domain = 'https://answers.ea.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
images = soup.find_all('a', class_='lia-link-navigation attachment-link')
print(images)
base_url = domain

for img in images:
    download_url = img.find('span')['li-download-url']
    full_url = urljoin(base_url, download_url)
    print(full_url)
    image = requests.get(full_url)
    with open('image.jpg', 'wb') as file:
        file.write(image.content)
        file.close()


num_pepole_has_same_issue = soup.find('a', class_='lia-link-navigation lia-rating-value-summary').text[0]
print(int(num_pepole_has_same_issue))





# save html 
with open('test.html', 'w') as file:
    file.write(response.text)
    file.close()


