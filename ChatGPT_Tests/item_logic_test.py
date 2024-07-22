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

# How many times do you want to ask the same question for each picture (to account for natural variance in response)
loops = 3

# Generating items for recipe / craft
target = 'ratattouille'

target_question = "I want to make " + target + ". What would I need? Only include items, no steps, processes, or amounts. List the items as words seperated by new lines all lowercase. Only include only the most common/traditional items"

headers1 = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload1 = {
  "model": "gpt-4o",
  "messages": [
  {
      "role": "user",
      "content": [
      {
          "type": "text",
          "text": target_question
      }
      ]
  },
  ],
  "max_tokens": 1000
}

recipe_response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers1, json=payload1)
recipe_string = str(recipe_response.json()["choices"][0]["message"]["content"])
recipe_items_original = recipe_string.splitlines()

# Formatting recipe items 
for i in range(len(recipe_items_original)):
  recipe_items_original[i] = recipe_items_original[i].strip().strip('\n')

previous_file_state = ''
try:
  recipe_file = open(rootdir + '/recipes/' + target + ".txt", 'r')
  previous_file_state = recipe_file.read()
  recipe_file.close()
except:
  pass
  
recipe_file = open(rootdir + '/recipes/' + target + ".txt", 'w')

# Write results of recipe to a .txt file
now = datetime.datetime.now()
recipe_file.write('Time: ' + str(now) + '\n')
recipe_file.write('Question: ' + target_question + '\n')
recipe_file.write('Response: \n{\n' + recipe_string + '\n}\n\n')
recipe_file.write('------------------------------------------\n\n')
recipe_file.write(previous_file_state)
recipe_file.close()

# Looping through each file in images folder
for subdir, dirs, files in os.walk(rootdir + '/images'):
    for file in files:
      # Creates/adds to a .txt file of the same name to store the results we get from chatgpt
      try:
        output = open(rootdir + '/image_logic_results/'+ os.path.splitext(file)[0] + '.txt', 'r+')
      except:
        output = open(rootdir + '/image_logic_results/'+ os.path.splitext(file)[0] + '.txt', 'w')
      output.close()

      # Path to your image
      image_path = os.path.join(subdir, file)

      # Getting the base64 string
      base64_image = encode_image(image_path)

      question = "I want to make " + target + ". What would I need? Just think about it. Now, are there any items in the picture that I would need? Ignore branding and numbers. Return answers in the form of words seperated by new lines, all lowercase. If not, return n/a. Take your time and double check the image for items."

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
                  "url": f"data:image/jpeg;base64,{base64_image}",
                  "detail": "low"
                }
            }
            ]
        }
        ],
        "max_tokens": 1000
        
      }


      # Checks if there's a corresponding .items file for the image
      # If not, it will skip the image and not generate any results
      try:
        image_items_original = open(rootdir + '/items/' + os.path.splitext(file)[0] + '.items', 'r').readlines()
        # Readlines does not strip the '\n' so here we manually do it
        for i in range(len(image_items_original)):
          image_items_original[i] = image_items_original[i].strip().strip('\n')     
      except Exception as e:
        print(os.path.splitext(file)[0] + " did not have a corresponding .items file, skipping image!")
        print(e)
        continue
      

      # Asking the same question "loops" amount of times
      for loop in range(loops):
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
        
        output = open(rootdir + '/image_logic_results/'+ os.path.splitext(file)[0] + '.txt', 'r+')
        # Remember previous file state to prepend new data and erase
        previous_file_state = output.read()
        output.truncate(0)
        output.seek(0)

        # Data formatting / setup
        true_positive = []
        true_negative = []
        false_positive =  []
        false_negative = []
        response_items = []

        # Recording words that have been used. Used to determine the false and true negatives
        image_item_used = []
        recipe_item_used = []

        # Sometimes I get errors when sending certain pictures, just used a catch so it won't interrupt the remaining images
        recipe_items = recipe_items_original[:]
        image_items = image_items_original[:]

        try:
          for item in response.json()['choices'][0]['message']['content'].splitlines():
            response_items.append(item.strip().strip('\n'))
        except:
          print('\n' + file + " encountered a problem!")
          print(response.json())
          print('\n')
          continue

        # Check for no items in image match
        if response_items[0] == 'n/a':
          response_items.remove('n/a')
        
        print(response_items)
        print(image_items)
        print(recipe_items)
        # Autograder
        for response_item in response_items:
          in_image = False
          for image_item in image_items:
            print("Testing " + image_item + " with " + response_item)
            if image_item in response_item:
              print('match!')
              # Gpt item is actually in the image
              image_item_used.append(image_item)
              in_recipe = False
              in_image = True
              for recipe_item in recipe_items:
                if image_item in recipe_item:
                  # Gpt response is in the recipe and image
                  recipe_item_used.append(recipe_item)
                  true_positive.append(response_item + '\t(' + image_item + ', ' + recipe_item + ')')
                  in_recipe = True
                  break
              
              # Gpt response in image, not in recipe
              if not in_recipe:
                false_positive.append(response_item + '\t(' + image_item + ' not in recipe)')
              
              break
            
          # Gpt response not in image
          if not in_image:
            false_positive.append(response_item + '\t(not in image)')
        
        # Removing image and recipe items that were identified
        for item in image_item_used:
          try:
            image_items.remove(item)
          except:
            pass
        
        for item in recipe_item_used:
          try:
            recipe_items.remove(item)
          except:
            pass
        
        # Checking if gpt missed any items
        for image_item in image_items:
          for recipe_item in recipe_items:
            if image_item in recipe_item:
              false_negative.append(recipe_item + '(' + image_item + ')')
              recipe_items.remove(recipe_item)
        
        true_negative = recipe_items

        # Formatting of response and writing to file
        now = datetime.datetime.now()
        output.write('Time: ' + str(now) + '\n')
        output.write('Question: ' + question + '\n')
        output.write('Response: \n{\n' + str(response.json()["choices"][0]["message"]["content"]) + '\n}\n\n')
        
        
        output.write('True Positive [' + str(len(true_positive)) + ']:\n')
        for item in true_positive:
          output.write('\t' + item + '\n')
        output.write('\n')

        output.write('False Positive [' + str(len(false_positive)) + ']:\n')
        for item in false_positive:
          output.write('\t' + item + '\n')
        output.write('\n')

        output.write('True Negative [' + str(len(true_negative)) + ']:\n')
        for item in true_negative:
          output.write('\t' + item + '\n')
        output.write('\n')

        output.write('False Negative [' + str(len(false_negative)) + ']:\n')
        for item in false_negative:
            output.write('\t' + item + '\n')
        output.write('\n')
        
        output.write('\n---------------------------------------------------\n\n' + previous_file_state)
        
        print(file + " completed! #" + str(loop + 1))
    
        output.close()
      
        




