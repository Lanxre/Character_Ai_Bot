import json
import logging
import os

from aiogram.client.session import aiohttp


from core.internal.schemas import ChatCompletionContent


async def fetch_completion(
		system_message: str,
		user_message: str
) -> ChatCompletionContent:
	messages = [
		{"role": "system", "content": system_message},
		{"role": "user", "content": user_message}
	]
	endpoint = os.getenv("ENDPOINT")
	headers = {
		'accept': 'application/json',
		'Content-Type': 'application/json'
	}
	data = {
		'model': 'gpt-3.5-turbo',
		'messages': messages,
	}
	try:
		async with aiohttp.ClientSession() as session:
			async with session.post(endpoint, headers=headers, data=json.dumps(data)) as response:
				resp_data = await response.json()
				return ChatCompletionContent(
					id=resp_data['id'],
					content=resp_data['choices'][0]['message']['content']
				)
	except Exception as e:
		logging.error(f"An error occurred: {e}")

	return ChatCompletionContent(id='', content='')
