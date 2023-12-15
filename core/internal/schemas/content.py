from pydantic import BaseModel


class ChatCompletionContent(BaseModel):
	id: str
	content: str

