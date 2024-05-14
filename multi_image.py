import os
import ollama


#model = 'llava-llama3'
model = 'llava-phi3'
output_directory = 'output'
file_name = f"output_ollama_{model}.txt"
file_path = os.path.join(output_directory, file_name)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
# Pull the llava-llama3 model
ollama.pull(model)

# Directory containing images
image_dir = './frames'  # Specify the directory containing the images

# List of images (JPG and PNG)
image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.jpg') or f.endswith('.png')]

# Initial prompt
prompt = 'Summarize the image, specially focus on people or vehicle if there is any'

# Accumulator for context
context = ''

# Loop over each image
for image_path in image_paths:
    # Perform inference
    res = ollama.chat(
        model="llava-llama3",
        messages=[
            {
                'role': 'user',
                'content': f'Context: {context} Prompt: {prompt}',
                'images': [image_path]
            }
        ]
    )

    # Print the text output
    print("Output:")
    output = res['message']['content']
    print(output)
    print("****************")
    # Save the output to a text file
    with open(file_path, 'a') as file:
        file.write(output+'\n'+'**********'+'\n')

    # Update context
    context += output

    # Update prompt for the next iteration
    prompt = context+'\n'+prompt
    #print("current prompt:", prompt)
    #print("---------------")