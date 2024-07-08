import json
import datetime
import os

outf = open('ChatGPT_Tests/responses/testing.txt', 'w')

rootdir = 'C:\\Users\\geodz\\OneDrive\\Documents\\Coding\\School Projects\\CU Boulder\\Correl Lab\\ChatGPT_Tests\\images'

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        outf.write(os.path.splitext(file)[0] + "\n")

# start_index = response.find('\"content\": \"')
# end_index = response.find('\"', start_index + 15)
# print(start_index)
# print(end_index)
# print(response[start_index:end_index + 1])



