import datetime
import requests
import base64
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

api_key=os.getenv("OPENAI_API_KEY")

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')


# What do you want to ask about the picture
question = "What items are in the image? Ignore branding. Return answers in the form of words seperated by new lines"

# Path to your image
image_path = 'ChatGPT_Tests\images\produce\\lemon_lime.jpg'

# Getting the base64 string
base64_image = encode_image(image_path)

# Full Request
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

# Request and store responce
response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

# Save in file, puts recived data in front
previous_file_state = ''
with open('ChatGPT_Tests/test_questions.txt', 'r') as f:
    previous_file_state = f.read()

with open('ChatGPT_Tests/test_questions.txt', 'w') as f:
    now = datetime.datetime.now()
    f.write('Time: ' + str(now) + '\n')
    f.write('File: ' + os.path.splitext(image_path)[0] + '\n')
    f.write('Question: ' + question + '\n')
    f.write('Response: \n{\n' + response.json()["choices"][0]["message"]["content"] + '\n}\n\n\n\n')
    f.write(previous_file_state)




