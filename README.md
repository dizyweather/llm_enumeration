# LLM_Enumeration

<p>
  LLM_Enumeration is a repo where I'm testing ChatGPT4o in it's ability in understanding images. 
</p>

The files here basically help automate sending requests and grading of the responses to/from chatgpt. It only *helps* automate grading because due to chatgpt's natural variance in response, you will still have to look through the responses yourself to collect accurate data.


## Packages/Setup
<p>Packages Used:</p>

```bash
pip install openai
pip install requests
```
<p>
  I'm using python 3.9 but i'm pretty sure using other versions won't affect it.<br> 
  Since we're sending requests to openai you will need to create a .env file and place your api key in it like so:
</p>

```.env
OPENAI_API_KEY = YOUR_KEY_HERE
```

## Usage
### ```item_identification_test.py```

This file will be testing the general capabilities of ChatGpt4o in it's ability to just identify items in an image. 

To summarize, this file will loop through all images in the ```images``` folder and send a request with the image and question to chatgpt.<br>
After it recieves a response, it will check if there is a corresponding .items file of the image. If so, it will autograde the response.<br>
Then it will print data about the request and autograding (if applicable) into a corresponding .txt file with the same name as the image in the ```image_id_results``` folder.<br>

So to use this file:
- Replace the ```images``` folder with your own folder of images.
-  For each image you want to autograde, make a corresponding .items file with the ***same name*** in the ```items``` folder
   - Make sure it lists all items actually in the image, all lowercase, and one item each line.
   - Try not to add spaces at the beggining/end or empty lines between items, I don't think I stripped the input.
- Edit the ```question = "____"``` variable with any specifics/helping info for gpt.
- Edit the ```loops = #``` variable to set how many times you want to ask the same question for each image.

After running, the terimal will have print statements to let you know how far along is it.<br>
After done, you can check the ```image_id_results``` and you'll see a .txt file for each of your images. The file will list every request sent to gpt with: 
- Time when response was processed
- Question the request to gpt was sent with
- Response from gpt
- Summary from the autograder
  - (If there's a corresponding .items file)

After, you can run ```count_id_results.py``` which will loop through the ```image_id_results``` folder and sum up all the items in the Identified, Unsure, and Missed sections together for each image into a corresponding .sum file in the ```image_id_summary``` folder.

**About Autograding:**

> The autograder will loop through each line of the response and compare it to see if any of the correct items match. This is done by a basic ```string in string``` comparison. If there is a match, the corresponding response will be put into the **Identified** section. If there are no match for a response, it will be put into the **Unsure** section. And if there are some answers that weren't used, they'll be put in the **Missed** section.
<br>

### ```item_logic_test.py```
This file will be testing the logical reasoning of chatgpt with identification. The previous program is very basic, we just ask for all items in the image. However, it's more useful if we ask gpt to look for items that meet a certain criteria, say a recipe. This program asks gpt to identify items that we would need for a given recipe/craft. It follows the format: <br>

>I want to make ______. Are there any items in the picture that I would need?

Now to summarize how this file will work:
1. It will first send a request to gpt asking what items would be needed to make the target craft/recipe.
2. After recieving the response, it will be writtent to the ```recipes``` folder so you can check it later.
3. Then, it will loop through each image and ask if there are any items in the image that you would need to make the target craft/recipe
4. After recieving the response, it will compare the answers to the recipe and the actual items in the picture from the corresponding .items file.
5. Finally, it will print the results to a corresponding .txt file to the ```image_logic_results``` file

To use the file:
- Replace the ```images``` folder with your own folder of images.
- Edit the ```target = "____"``` to whatever you want
- Edit the ```target_question = "____"``` to whatever you want
  - This is the prompt to ask gpt for the recipe
- Edit the ```loops = #``` for how many times you ask each image the question
- If an image doesn't have a .items file, it will be skipped over.

After completion, the results will be printed with basically the same format as in the ```item_identification_test.py``` program.

Will also make a count program to sum up the results in the future like in the previous program.



## License

[MIT](https://choosealicense.com/licenses/mit/)
