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
### item_identification_test.py

This file will be testing the general capabilities of ChatGpt4o in it's ability to just identify items in an image. 

To summarize, this file will loop through all images in the ```images``` folder and send a request with the image and question to chatgpt.<br>
After it recieves a response, it will check if there is a corresponding .items file of the image. If so, it will autograde the response.<br>
Then it will print data about the request and autograding (if applicable) into a corresponding .txt file with the same name as the image in the ```image_id_results``` folder.<br>

So to use this file:
1. Replace the ```images``` folder with your own folder of images.
2. For each image you want to autograde, make a corresponding .items file with the ***same name*** in the ```items``` folder
   - Make sure it lists all items actually in the image, all lowercase, and one item each line.
   - Try not to add spaces at the beggining/end or empty lines between items, I don't think I stripped the input.
3. Edit the ```question = "____"``` variable with any specifics/helping info for gpt.
4. Edit the ```loops = #``` variable to set how many times you want to ask the same question for each image.
5. Run

After running, the terimal will have print statements to let you know how far along is it.<br>
After done, you can check the ```image_id_results``` and you'll see a .txt file for each of your images. The file will list every request sent to gpt with: 
- Time when response was processed
- Question the request to gpt was sent with
- Response from gpt
- Summary from the autograder
  - (If there's a corresponding .items file)


**More about autograding:**

> The autograder will loop through each line of the response and compare it to see if any of the correct items match. This is done by a basic ```string in string``` comparison. If there is a match, the corresponding response will be put into the **Identified** section. If there are no match for a response, it will be put into the **Unsure** section. And if there are some answers that weren't used, they'll be put in the **Missed** section.
<br>

In the future i'll probably make a sum program that will loop through the files in the ```image_id_results``` folder and grouping same words and summing them up to make a big result file so you won't have to scroll through each request to gpt.

### item_logic_test.py
This file will be testing the logical reasoning of chatgpt with identification. The previous program is very basic, we just ask for all items in the image. However, it's more useful if we ask gpt to look for items that meet a certain criteria, say a recipe. This program asks gpt to identify items that we would need for a given recipe/craft. It follows the format: <br>

>I want to make ______. Are there any items in the picture that I would need?





## License

[MIT](https://choosealicense.com/licenses/mit/)
