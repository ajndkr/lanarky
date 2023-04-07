# FastAPI Chat Application

This is a simple FastAPI application for langchain agents with `streaming=True`.

## Setup Instructions

This project is built with Python 3.9. Clone this repository and follow the steps below to get started.

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

**Note**: The `requirements.txt` file is generated using `pip-tools`. If you want to add a new dependency, add it to `requirements.in` and run `pip-compile` to generate the `requirements.txt` file.

## CI/CD

This project uses `pre-commit` to run code linters before every commit. To install the pre-commit hooks, run the following commands:

```bash
pip install pre-commit
pre-commit install
```
