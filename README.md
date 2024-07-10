# LLM_Enumeration

<p>
  LLM_Enumeration is a repo where I'm testing ChatGPT4o in it's ability in understanding images. 
</p>
<p>
  The files here basically help automate sending requests and grading of the responses to/from chatgpt. It only *helps* automate grading because due to chatgpt's natural variance in response, you will still have to look through the responses yourself to collect accurate data.
</p>

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
### item_identification.py

<p>This file will be testing the question:</p>

><strong><p style="text-align: center;">"What items are in the image? Ignore branding and numbers. Return answers in the form of words seperated by new lines and all lowercase."</p> </strong>

<p>
  To summarize, this file will loop through all images in the <strong><i>images</i></strong> folder and send a request with the image and question to chatgpt.<br>
  When it recieves a response, it will check if there is a corresponding .items folder of the image. If so, it will autograde the response.<br>
  Then it will print data about the request and autograding (if applicable) into a corresponding .txt file with the same name as the image in the <strong><i>response</i></strong> folder.
</p>

**More about autograding:**

> For the autograder portion of this program to work, for each image in the <strong><i>images</i></strong> folder you want to be autograded, you must create a corresponding .items file (with the same name as the image) in the <strong><i>items</i></strong> folder. This file should contain the "correct" items seperated by newlines. The autograder will loop through each line of the response and compare it to see if any of the correct items match. This is done by a simple string in string comparison.<br> If there is a match, the corresponding response will be put into the **Identified** section. If there are no match for a response, it will be put into the **Unsure** section. And if there are some answers that didn't match, they'll be put in the **Missed** section.




## License

[MIT](https://choosealicense.com/licenses/mit/)
