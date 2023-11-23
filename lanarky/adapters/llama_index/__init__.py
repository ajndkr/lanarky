from importlib.util import find_spec

if not find_spec("llama_index"):
    raise ImportError(
        "run `pip install lanarky[llama-index]` to use the llama-index adapter"
    )
