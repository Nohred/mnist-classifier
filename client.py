import requests
import os
url = 'http://127.0.0.1:3000/predict'

image_path = 'kuatro.png'

with open(image_path, 'rb') as image_file:
    image_bytes = image_file.read()

response = requests.post(url, files={'file': image_bytes})

if response.status_code == 200:
    print(response.json())
