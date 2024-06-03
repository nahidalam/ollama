import os
import time
import ollama

# Start time
start_time = time.time()

model = 'llava-llama3'
#model = 'llava-phi3'
#model = 'llava'
output_directory = 'output'
file_name = f"output_ollama_{model}.txt"
file_path = os.path.join(output_directory, file_name)
if not os.path.exists(output_directory):
    os.makedirs(output_directory)
# Pull the model. TODO: do not need it after first time, make it part of installation
#ollama.pull(model)

# Directory containing images
image_dir = './frames'  # Specify the directory containing the images

# List of images (JPG and PNG)
image_paths = [os.path.join(image_dir, f) for f in os.listdir(image_dir) if f.endswith('.jpg') or f.endswith('.png')]

# Initial prompt
prompt = 'Summarize the image only if there is any person or vehicle'

# Accumulator for context
#context = ''

# Loop over each image
for image_path in image_paths:
    # Get image file name with extension
    image_file_name = os.path.basename(image_path)

    # Perform inference
    res = ollama.chat(
        model="llava-llama3",
        messages=[
            {
                'role': 'user',
                'content': f'{prompt}',
                'images': [image_path]
            }
        ]
    )

    # Print the text output
    print("Output:")
    output = res['message']['content']
    print(output)
    print("****************")
    # Save the image file name and output to a text file
    with open(file_path, 'a') as file:
        file.write("Image File: " + image_file_name + '\n')
        file.write(output+'\n'+'**********'+'\n')

# Write total execution time and final prompt at the end of the file
with open(file_path, 'a') as file:
    file.write("\nTotal Execution Time: " + str(time.time() - start_time) + " seconds\n")
    file.write("Prompt Used: " + prompt)

# End time
end_time = time.time()

# Calculate execution time
execution_time = end_time - start_time
print("Execution Time:", execution_time, "seconds")
