import requests
import datetime
import base64
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

from PIL import Image


api_key=os.getenv("OPENAI_API_KEY")

# Function to encode the image
def encode_image(image_path):
  # image = Image.open(image_path)
    
  # # next 3 lines strip exif
  # data = list(image.getdata())
  # image_without_exif = Image.new(image.mode, image.size)
  # image_without_exif.putdata(data)
      
  # image_without_exif.save('image_file_without_exif.jpeg')

  # # as a good practice, close the file handler after saving the image.
  # image_without_exif.close()
  
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to the root directory of wherever you chose to put this repo.
rootdir = os.path.dirname(os.path.realpath(__file__))

# Prompt to be sent along with the image 
prompt = "What items are in the image? Ignore branding and numbers. Return answers in the form of words seperated by new lines and all lowercase."

# How many times do you want to ask the same prompt for each picture (to account for natural variance in response)
loops = 10

# Looping through each file in images folder
for subdir, dirs, files in os.walk(rootdir + '/images'):
    for file in files:
      # Makes sure that there is a .txt file of the same name to store the results we get from chatgpt
      try:
        output = open(rootdir + '/image_id_results/'+ os.path.splitext(file)[0] + '.txt', 'r+')
      except:
        output = open(rootdir + '/image_id_results/'+ os.path.splitext(file)[0] + '.txt', 'w')
      
      output.close()
     
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
                "text": prompt
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
        
        # Get previous file state
        output = open(rootdir + '/image_id_results/'+ os.path.splitext(file)[0] + '.txt', 'r+')
        previous_file_state = output.read()
        output.truncate(0)
        output.seek(0)
        
        # Data formatting / setup
        identified = []
        missed = []
        data =  []
        
        try:
          for item in response.json()["choices"][0]["message"]["content"].splitlines():
            data.append(item.strip().strip('\n'))
        except:
          print('\n' + file + " encountered a problem! Skipping this loop!")
          print(response.json())
          print(os.stat(image_path).st_size)
          print('\n')
          continue

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
        output.write('Prompt: ' + prompt + '\n')
        try:
          output.write('Response: \n{\n' + str(response.json()["choices"][0]["message"]["content"]) + '\n}\n\n')
        except:
          output.write('Response: \n{\n' + "Encountered problem converting json to string!" + '\n}\n\n')
          print('\n' + file + " encountered a problem!")
          print(response.json())
          print('\n')
          
        
        
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
        




