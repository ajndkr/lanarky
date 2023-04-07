from fastapi import APIRouter, Response, status
from fastapi.responses import StreamingResponse
from app.utils import generate_chat_messages

router = APIRouter()

@router.get("/chat")
async def chat():
    async def generate():
        async for message in generate_chat_messages():
            yield message

    headers = {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
    }

    return StreamingResponse(generate(), headers=headers)