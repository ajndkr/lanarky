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
-d '{"query": "Give me list samples with code", "history": [ ["What is a Text Embedding Model?", "Text embedding models are machine learning algorithms that convert text into numerical representations called embeddings. These embeddings are useful for a variety of tasks, such as natural language processing, sentiment analysis, and text classification. Text embedding models use a variety of techniques, such as word embedding, sentence embedding, and document embedding."],     ["List a types of text embeddings", "Text embeddings are a type of representation that maps words, phrases, or sentences from a language to a vector of real numbers. There are several types of text embeddings, including: Word Embeddings: Word embeddings map words to a vector of real numbers. These vectors capture the semantic meaning of the words and can be used to compare words to one another."] ]}' \
http://localhost:8000/chat
```

### Gradio UI

Open http://localhost:8000/gradio in your browser to access the Gradio UI.

### Websocket Testing

Open http://localhost:8000 in your browser to access the chatbot UI with websocket support.
