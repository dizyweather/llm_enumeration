# LLM_Enumeration


LLM_Enumeration is a repo where I'm testing ChatGPT4o in it's ability in understanding images and how different prompts affect accuracy. The main usage of this repo is to test different prompts on their effectiveness in making a LLM/VLM identify specific objects in an image. To do so, the files here automate sending prompts and grading responses. 

**NOTE**：These files only *help* automate grading. Due to LLMs/VLMs natural variance in response, you will still have to look through the generated summary files to make sure the autograder was accurate. 

You can test a different llm/vlm by replacing the requests.post(), header, and payload. The autograder will still work if you follow the format below. But for me, I'm testing ChatGPT4o.

## Packages/Setup
<p>Packages Used:</p>

```bash
pip install openai
pip install requests
```
<p>
  I'm using python 3.9 but i'm pretty sure using other versions won't affect it.<br> 
  Since we're sending requests to openai's api you will need to create a .env file and place your api key in it like so:
</p>

```.env
OPENAI_API_KEY = YOUR_KEY_HERE
```

## Usage
### ```item_identification_test.py```

This file is used to test the general ability in identifying objects in an image. This program will return data in the form of indentified, missed, and unsure items.

To summarize how this file works:
1. This file will loop through all images in the ```images``` folder and send a request with the image and prompt to chatgpt.<br>
2. After it recieves a response, it will check if there is a corresponding ```.items``` file for the image. <br>
3. If so, it will autograde the response, using that file as the answers, into a **Identified**, **Unsure**, and **Missed** sections.<br>
4. Then it will print data about the request, response, and autograding (if applicable) into a corresponding ```.txt``` file with the same name as the image in the ```image_id_results``` folder.<br>

To use this file:
- Replace the ```images``` folder with your own folder of images.
- For each image you want to autograde, make a corresponding ```.items``` file with the ***same name*** in the ```items``` folder
   - This file should contain the actual items in the image (the answers) with each item having it's own line.
- Edit the ```prompt = "____"``` variable to whatever prompt you want to test.
- Edit the ```loops = #``` variable to set how many times you want to ask the same prompt for each image.

After, run ```count_id_results.py``` which will loop through the ```image_id_results``` folder and sum up all the items in the **Identified**, **Unsure**, and **Missed** sections together for each image into a corresponding .sum file in the ```image_id_summary``` folder.

**About Autograding:**

> The autograder will first retrieve the answers from the ```.items``` file. Then it will loop through each line of the response and compare it to see if it matches any of the answers. This is done by a basic ```string in string``` comparison. If there is a match, the corresponding response will be put into the **Identified** section. If there are no match for a response, it will be put into the **Unsure** section. And if there are some answers that weren't used, they'll be put in the **Missed** section.
<br>

### ```item_logic_test.py```
This file tests identification using logical reasoning. This program will return data in the form of a confusion matrix.

The previous program is very basic, we just ask for all items in the image. However, it's more useful if we ask gpt to look for items that meet a certain criteria, say a recipe. This program asks gpt to identify items that we would need for a given recipe/craft. It follows the format: <br>

I want to make ______. Are there any items in the picture that I would need?

Now to summarize how this file will work:
1. It will first send a request to gpt asking what items would be needed to make the target craft/recipe.
2. After recieving the response, it will be written to the ```recipes``` folder so you can check it later.
3. Then, it will loop through each image and ask if there are any items in the image that you would need to make the target craft/recipe
4. After recieving the response, it will compare the answers to the recipe and the actual items in the picture from the corresponding .items file.
5. Finally, it will print the results to a corresponding .txt file to the ```image_logic_results``` file

I use ChatGPT to generate the recipe list becuase through personal testing, it is pretty accurate. However, you can also remove that section of the program and make your own ```.txt``` file with the answers you want.

To use the file:
- Replace the ```images``` folder with your own folder of images.
- Edit the ```target = "____"``` to your target recipe/craft.
- Edit the ```target_prompt = "____"``` to affect how the recipe is generated.
- Edit the ```prompt = "____"``` to test your prompt.
- Edit the ```loops = #``` for how many times you ask each image the question
- Make a ```.items``` file for each image like in the previous program. If there is no file, it will skip the image.

Then run ```count_logic_results.py``` which will loop through the ```image_logic_results``` folder and sum up all the confusion matrix data together for each image into a corresponding ```.sum``` file in the ```image_logic_summary``` folder.

**About Autograding:**
> How response items are classified (Also using ```string in string```):
> 
> **True Positive**:  Response item is in the image and in the recipe
> 
> **False Positive**:  Response item is either not in the recipe or not found in the image
> 
> **True Negative**:  There is no response for an item in the recipe that **IS NOT** in the image
> 
> **False Negative**:  There is no response for an item in the recipe that **IS** in the image


## License

[MIT](https://choosealicense.com/licenses/mit/)
