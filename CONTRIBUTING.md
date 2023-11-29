This document contains information about contributing to this repository. Please read it before contributing.

## Setup Instructions

`lanarky` is built with Python 3.9 and managed by Poetry.
Clone this repository and follow the steps below to get started.

### Create conda environment:

```bash
conda create -n lanarky python=3.9 -y
conda activate lanarky
```

You can choose any other environment manager of your choice.

### Install Poetry:

```bash
pip install poetry
```

### Install Lanarky:

```bash
poetry install --all-extras
```

## Pre-Commit

`lanarky` uses `pre-commit` to run code checks and tests before every commit.

To install the pre-commit hooks, run the following commands:

```bash
poetry run pre-commit install
```

To run the pre-commit hooks on all files, run the following command:

```bash
make pre-commit
```

## Bump Version

Lanarky uses Makefile to bump versions:

```bash
make bump
```

Note: The make recipe bumps version and auto-commits the changes.
