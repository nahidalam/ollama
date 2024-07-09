'''
TODO: keep alive for faster response
'''

import requests
import base64
import sys
import json


def convert_image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode('utf-8')
        return base64_string



def concatenate_response_content(response_text):
    concatenated_content = ""
    for line in response_text.splitlines():
        try:
            json_line = json.loads(line)
            concatenated_content += json_line["message"]["content"]
        except json.JSONDecodeError:
            pass
    return concatenated_content


# Path to your image file
image_path = sys.argv[1]
base64_string = convert_image_to_base64(image_path)
prompt='Describe the person in the image in 1 sentence, with upper and lower body clothing color and their environment. Do not describe gender or race'


# Define the JSON data inline
json_data = {
    "model": "llava-llama3",
    "messages": [
        {
            "role": "user",
            "content": prompt,
            "images": [base64_string],
            "stream": False
        }
    ]
}

# Send the POST request using requests library
response = requests.post("http://localhost:11434/api/chat", json=json_data)

# Concatenate the response content
concatenated_content = concatenate_response_content(response.text)

# Print the concatenated content
#print("Concatenated Response Content:")
print(concatenated_content)

