from abc import abstractmethod
from typing import Generator

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str = Field(pattern=r"^(user|assistant)$")
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
        **create_kwargs,
    ):
        super().__init__(client=client)

        self.model = model
        self.stream = stream
        self.create_kwargs = create_kwargs

    async def stream_response(
        self, messages: list[Message]
    ) -> Generator[str, None, None]:
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

    async def __call__(self, messages: list[Message]) -> ChatCompletion:
        return await self._client.chat.completions.create(
            messages=messages,
            model=self.model,
            **self.create_kwargs,
        )
