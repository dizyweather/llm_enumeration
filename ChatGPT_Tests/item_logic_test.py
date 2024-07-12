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

# Path to the root directory of wherever you chose to put this repo.
rootdir = os.path.dirname(os.path.realpath(__file__))

# Question to be sent along with the image 
dish = 'spaghetti and meatballs'
question = "I want to make " + dish + ". Are there any items in the picture that I would need? Ignore branding and numbers. Return answers in the form of words seperated by new lines and all lowercase."

# How many times do you want to ask the same question for each picture (to account for natural variance in response)
loops = 1

# Looping through each file in images folder
for subdir, dirs, files in os.walk(rootdir + '/images'):
    for file in files:
      # Creates/adds to a .txt file of the same name to store the results we get from chatgpt
      output = open(rootdir + '/results/'+ os.path.splitext(file)[0] + '.txt', 'w')
      output = open(rootdir + '/results/'+ os.path.splitext(file)[0] + '.txt', 'r+')
      
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

      
      # Trys to open the corresponsing .items file of the image.
      # If there are none, we'll skip the autograding feature.
      try:
        answers = open(rootdir + '/items/' + os.path.splitext(file)[0] + '.items', 'r').readlines()
        print('opened: ' +  os.path.splitext(file)[0])
        autograde = True
        
      except Exception as e:
        autograde = False
        answers = []
        

      for loop in range(loops):
        print('hit')
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        
        # Remember previous file state to prepend new data
        previous_file_state = output.read()
        
        # Data formatting / setup
        correct_positive = []
        correct_negative = []
        false_positive =  []
        false_negative = []
        
        data = []
        for item in response.json()["choices"][0]["message"]["content"].splitlines():
          data.append(item)

        # Autograding
        # TODO

        # Formatting of response and writing to file
        now = datetime.datetime.now()
        output.write('Time: ' + str(now) + '\n')
        output.write('Question: ' + question + '\n')
        output.write('Response: \n{\n' + str(response.json()["choices"][0]["message"]["content"]) + '\n}\n\n')
        
        if autograde:
          output.write('Correct Positive [' + str(len(correct_positive)) + ']:\n')
          for item in correct_positive:
              output.write('\t' + item + '\n')
          output.write('\n')

          output.write('Fasle Positive [' + str(len(false_positive)) + ']:\n')
          for item in false_positive:
              output.write('\t' + item + '\n')
          output.write('\n')

          output.write('Correct Negative [' + str(len(correct_negative)) + ']:\n')
          for item in correct_negative:
              output.write('\t' + item + '\n')
          
          output.write('Fasle Negative [' + str(len(false_negative)) + ']:\n')
          for item in false_negative:
              output.write('\t' + item + '\n')
          output.write('\n')
        
        output.write('\n---------------------------------------------------\n\n' + previous_file_state)
        
        print(file + " completed! #" + str(loop))
      output.close()
        




