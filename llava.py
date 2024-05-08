import ollama
ollama.pull('llava-llama3')
res = ollama.chat(
	model="llava-llama3",
	messages=[
		{
			'role': 'user',
			'content': 'Describe this image:',
			'images': ['./art.jpg']
		}
	]
)

print(res['message']['content'])
