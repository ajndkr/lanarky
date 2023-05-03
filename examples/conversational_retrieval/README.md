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
-d '{
    "query": "Give me a code sample",
    "history": [
        [
            "What is a Text Splitter?",
            "Text Splitter is a module that is responsible for breaking up a document into smaller pieces, or chunks, that can be more easily processed."
        ],
        [
            "List all text splitter supported",
            "Langchain provides several different text splitters to help with processing text data. These include the Character Text Splitter, Hugging Face Length Function, Latex Text Splitter, Markdown Text Splitter, NLTK Text Splitter, Python Code Text Splitter, RecursiveCharacterTextSplitter, Spacy Text Splitter, tiktoken (OpenAI) Length Function, and TiktokenText Splitter."
        ]
    ]
}' \
http://localhost:8000/chat
```

### Gradio UI

Open http://localhost:8000/gradio in your browser to access the Gradio UI.

### Websocket Testing

Open http://localhost:8000 in your browser to access the chatbot UI with websocket support.
