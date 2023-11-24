from importlib.util import find_spec

if not find_spec("openai"):
    raise ImportError("run `pip install lanarky[openai]` to use the openai adapter")
