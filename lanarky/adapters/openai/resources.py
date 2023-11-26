from abc import abstractmethod
from typing import Generator

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str = Field(pattern=r"^(user|assistant)$")
    content: str


class SystemMessage(BaseModel):
    role: str = "system"
    content: str


class OpenAIResource:
    def __init__(self, client: AsyncOpenAI = None):
        self._client = client or AsyncOpenAI()

    @abstractmethod
    async def stream_response(self, *args, **kwargs) -> Generator[str, None, None]:
        ...


class ChatCompletionResource(OpenAIResource):
    def __init__(
        self,
        *,
        client: AsyncOpenAI = None,
        model: str = "gpt-3.5-turbo",
        stream: bool = False,
        system: str = None,
        **create_kwargs,
    ):
        super().__init__(client=client)

        self.model = model
        self.stream = stream
        self.system = SystemMessage(content=system) if system else None
        self.create_kwargs = create_kwargs

    async def stream_response(self, messages: list[dict]) -> Generator[str, None, None]:
        messages = self._prepare_messages(messages)
        print(messages)
        data = await self._client.chat.completions.create(
            messages=messages,
            model=self.model,
            stream=self.stream,
            **self.create_kwargs,
        )

        if self.stream:
            async for chunk in data:
                if not isinstance(chunk, ChatCompletionChunk):
                    raise TypeError(f"Unexpected data type: {type(data)}")
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        else:
            if not isinstance(data, ChatCompletion):
                raise TypeError(f"Unexpected data type: {type(data)}")
            yield data.choices[0].message.content

    async def __call__(self, messages: list[dict]) -> ChatCompletion:
        messages = self._prepare_messages(messages)
        return await self._client.chat.completions.create(
            messages=messages,
            model=self.model,
            **self.create_kwargs,
        )

    def _prepare_messages(self, messages: list[dict]) -> list[dict]:
        if self.system is not None:
            messages = [self.system.model_dump()] + messages
        return messages
