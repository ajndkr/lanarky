from langchain import ConversationChain
from langchain.callbacks.base import AsyncCallbackManager
from langchain.chat_models import ChatOpenAI

from .callback import AsyncFastApiStreamingCallback


def load_conversation_chain() -> ConversationChain:
    return ConversationChain(
        llm=ChatOpenAI(
            temperature=0,
            streaming=True,
            callback_manager=AsyncCallbackManager([AsyncFastApiStreamingCallback()]),
        ),
        verbose=True,
    )
