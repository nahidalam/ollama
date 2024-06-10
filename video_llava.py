import ollama
ollama.pull('anas/video-llava:test')
res = ollama.chat(
	model="anas/video-llava:test",
	messages=[
		{
			'role': 'user',
			'content': 'Describe this video:',
			'images': ['/Users/nahalam/Documents/code/ai/ollama/rest_area.mp4']
		}
	]
)

print(res['message']['content'])
