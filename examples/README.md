# Lanarky Examples

This directory contains a list of demo examples of FastAPI applications for various langchain use cases.

## Overview

- [Setup Instructions](#setup-instructions)
- [Usage](#usage)
- [Demo Applications](#demo-applications)
  - [Conversation Chain](#conversation-chain)
  - [Retrieval QA with Sources Chain](#retrieval-qa-with-sources-chain)
  - [Conversational Retrieval](#conversational-retrieval)
  - [Zero Shot Agent](#zero-shot-agent)

## Setup Instructions

The app is built with Python 3.9. Clone this repository and follow the steps below
to get started.

### Create conda environment:

```bash
conda create -n demo-examples python=3.9 -y
conda activate demo-examples
```

You can choose any other environment manager of your choice.

### Install dependencies:

```bash
pip install -r requirements.txt
```

**Note**: The `requirements.txt` file is generated using `pip-tools`. To update the locked
requirements, update the `requirements.in` file and run `pip-compile requirements.in`. To upgrade
the dependencies, run `pip-compile --upgrade requirements.in`.

## Usage

### Run the application

To run a demo example, select the command based on the langchain use case you want to try out.

```
uvicorn app.<app_name>:app --reload
```

Jump to [Demo Applications](#demo-applications) section to see the list of available applications.

**Note**: You can also use the "Run & Debug" VSCode feature to run one of the applications.

![vscode-demo](../assets/vs_code_configs.png)

### Gradio UI

Open http://localhost:8000/gradio in your browser to access the Gradio UI.

### Websocket Testing

Open http://localhost:8000 in your browser to access the chatbot UI with websocket support.

## Demo Applications

### Conversation Chain

Start FastAPI server:

```bash
uvicorn app.conversation_chain:app --reload
```

#### Sample cURL request

```bash
curl -N -X POST \
-H "Accept: text/event-stream" -H "Content-Type: application/json" \
-d '{"query": "write me a song about sparkling water" }' \
http://localhost:8000/chat
```

### Retrieval QA with Sources Chain

Start FastAPI server:

```bash
uvicorn app.retrieval_qa_w_sources:app --reload
```

#### Sample cURL request

```bash
curl -N -X POST \
-H "Accept: text/event-stream" -H "Content-Type: application/json" \
-d '{"query": "Give me list of text splitters available with code samples" }' \
http://localhost:8000/chat
```

### Conversational Retrieval

Start FastAPI server:

```bash
uvicorn app.conversational_retrieval:app --reload
```

#### Sample cURL request

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

### Zero Shot Agent

Start FastAPI server:

```bash
uvicorn app.zero_shot_agent:app --reload
```

#### Sample cURL request

```bash
curl -N -X POST \
-H "Accept: text/event-stream" -H "Content-Type: application/json" \
-d '{"query": "what is the square root of 64?" }' \
http://localhost:8000/chat
```
