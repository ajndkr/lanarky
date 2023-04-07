from fastapi import FastAPI, Response, status
from fastapi.responses import StreamingResponse
from app.routes import router

app = FastAPI()

@app.get("/chat")
async def chat():
    async def generate():
        yield "Hello, world!"
    return StreamingResponse(generate(), media_type="text/plain")