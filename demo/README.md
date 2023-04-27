# FastAPI Demo Application

This is a simple FastAPI application for streaming LLM chains.

## Setup Instructions

The app is built with Python 3.9. Clone this repository and follow the steps below
to get started.

### Create conda environment:

```bash
conda create -n fastapi-async-langchain python=3.9 -y
conda activate fastapi-async-langchain
```

You can choose any other environment manager of your choice.

### Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Run the application

```bash
uvicorn app:app --reload
```

### Sample cURL request

```bash
curl -N -X POST \
-H "Accept: text/event-stream" -H "Content-Type: application/json" \
-d '{"query": "write me a song about sparkling water"}' \
http://localhost:8000/chat
```

![demo](../assets/demo.gif)

### Sample cURL request for retrieval qa with sources

```bash
curl -N -X POST \
-H "Accept: text/event-stream" -H "Content-Type: application/json" \
-d '{"query": "Give me list of text splitters available with code samples" }' \
http://localhost:8000/retrieval-qa-with-sources
```
