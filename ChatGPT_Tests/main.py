import requests
import datetime
import base64
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

api_key=os.getenv("OPENAI_API_KEY")

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Where you want to start looping through files
rootdir = os.path.dirname(os.path.realpath(__file__))

# What do you want to ask about the picture
question = "What items are in the image? Ignore branding. Return answers in the form of words seperated by new lines."

# How many times do you want to ask the same question (to account for natural variance in response)
loops = 1

# Looping through each file in images folder
for subdir, dirs, files in os.walk(rootdir + '\\images'):
    for file in files:
        # Creates/adds to a .txt file of the same name to store the results we get from chatgpt
        f = open(rootdir + '\\test\\'+ os.path.splitext(file)[0] + '.txt', 'a')
        
        # Path to your image
        image_path = os.path.join(subdir, file)

        # Getting the base64 string
        base64_image = encode_image(image_path)

        headers = {
          "Content-Type": "application/json",
          "Authorization": f"Bearer {api_key}"
        }

        payload = {
          "model": "gpt-4o",
          "messages": [
            {
              "role": "user",
              "content": [
                {
                  "type": "text",
                  "text": question
                },
                {
                  "type": "image_url",
                  "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                  }
                }
              ]
            }
          ],
          "max_tokens": 300
        }

        for i in range(loops):
          response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
          
          # Formatting of response and writing to file
          now = datetime.datetime.now()
          f.write('Time: ' + str(now) + '\n')
          f.write('Question: ' + question + '\n')
          f.write('Response: \n{\n' + response.json()["choices"][0]["message"]["content"] + '\n}\n\n\n\n')
          print(file + " completed!")




