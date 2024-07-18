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
question = "What items are in the image? Ignore branding and numbers. Return answers in the form of words seperated by new lines and all lowercase."

# How many times do you want to ask the same question for each picture (to account for natural variance in response)
loops = 3

# Looping through each file in images folder
for subdir, dirs, files in os.walk(rootdir + '/images'):
    for file in files:
      # Creates/adds to a .txt file of the same name to store the results we get from chatgpt
      output = open(rootdir + '/image_id_results/'+ os.path.splitext(file)[0] + '.txt', 'w')
      output.close()

      output = open(rootdir + '/image_id_results/'+ os.path.splitext(file)[0] + '.txt', 'r+')
     
      # Path to your image
      image_path = os.path.join(subdir, file)

      # Getting the base64 image
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
        "max_tokens": 1000
      }

      
      # Trys to open the corresponsing .items file of the image.
      # If there are none, we'll skip the autograding feature.
      try:
        answers = open(rootdir + '/items/' + os.path.splitext(file)[0] + '.items', 'r').readlines()
        # print('opened: ' +  os.path.splitext(file)[0])
        autograde = True
        
      except Exception as e:
        autograde = False
        answers = []
        

      for loop in range(loops):
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        
        previous_file_state = output.read()
        # Data formatting / setup
        identified = []
        missed = []
        data =  []
        
        for item in response.json()["choices"][0]["message"]["content"].splitlines():
          
          data.append(item.strip().strip('\n'))

        # Autograding
        for key_item in answers:
          key_item = key_item.strip('\n ')
          found = False
          i = 0
          while i < len(data):
              response_item = data[i]
              if key_item in response_item:
                  identified.append(response_item + ' (' + key_item + ')')
                  data.pop(i)
                  found = True
                  i = i - 1
              i = i + 1
              
          if not found:
              missed.append(key_item)

        # Formatting of response and writing to file
        now = datetime.datetime.now()
        output.write('Time: ' + str(now) + '\n')
        output.write('Question: ' + question + '\n')
        output.write('Response: \n{\n' + str(response.json()["choices"][0]["message"]["content"]) + '\n}\n\n')
        
        if autograde:
          output.write('Identified [' + str(len(identified)) + ']:\n')
          for item in identified:
              output.write('\t' + item + '\n')
          output.write('\n')

          output.write('Missed [' + str(len(missed)) + ']:\n')
          for item in missed:
              output.write('\t' + item + '\n')
          output.write('\n')

          output.write('Unsure [' + str(len(data)) + ']:\n')
          for item in data:
              output.write('\t' + item + '\n')
        
        output.write('\n---------------------------------------------------\n\n' + previous_file_state)
        
        # print to check progress in terminal
        print(file + " completed! #" + str(loop + 1))
      output.close()
        




