from importlib.util import find_spec

if not find_spec("langchain"):
    raise ImportError(
        "run `pip install lanarky[langchain]` to use the langchain adapter"
    )
