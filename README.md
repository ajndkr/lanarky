# FastAPI Chat Application

This is a simple FastAPI application for streaming LLM chains.

## Setup Instructions

This project is built with Python 3.9. Clone this repository and follow the steps below
to get started.

### Create conda environment:

```bash
conda create -n fastapi-langchain python=3.9
conda activate fastapi-langchain
```

You can choose any other environment manager of your choice.

### Install dependencies:

```bash
pip install -r requirements.txt
```

**Note**: The `requirements.txt` file is generated using `pip-tools`.
If you want to add a new dependency, add it to `requirements.in` and run
`pip-compile` to generate the `requirements.txt` file.

## Usage

### Run the application

```bash
uvicorn api.main:app --reload
```

### Sample cURL request

```bash
curl -N -X POST \
-H "Accept: text/event-stream" -H "Content-Type: application/json" \
-d '{"query": "write me a song about sparkling water"}' \
http://localhost:8000/chat
```

![demo](assets/demo.gif)

## CI/CD

This project uses `pre-commit` to run code linters before every commit.
To install the pre-commit hooks, run the following commands:

```bash
pip install pre-commit
pre-commit install
```

## Credits:

- https://gist.github.com/ninely/88485b2e265d852d3feb8bd115065b1a
- https://github.com/hwchase17/langchain/discussions/1706
