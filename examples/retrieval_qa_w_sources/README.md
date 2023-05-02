# RetrievalQA With Sources Chain Demo

This is a simple FastAPI application for streaming retrieval QA with sources chains.

## Setup Instructions

The app is built with Python 3.9. Clone this repository and follow the steps below
to get started.

### Create conda environment:

```bash
conda create -n retrieval-qa-with-sources-demo python=3.9 -y
conda activate retrieval-qa-with-sources-demo
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
-d '{"query": "Give me list of text splitters available with code samples" }' \
http://localhost:8000/chat
```

### Gradio UI

Open http://localhost:8000/gradio in your browser to access the Gradio UI.

### Websocket Testing

Open http://localhost:8000 in your browser to access the chatbot UI with websocket support.
