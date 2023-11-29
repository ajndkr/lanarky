from unittest.mock import MagicMock, create_autospec

import pytest
from fastapi import params
from langchain.chains import ConversationChain

from lanarky.adapters.langchain.dependencies import Depends


def test_depends_success():
    def mock_dependency():
        chain: ConversationChain = create_autospec(ConversationChain)
        chain.input_keys = ["input"]
        chain.output_keys = ["response"]
        return chain

    dependency = Depends(mock_dependency)
    assert isinstance(dependency, params.Depends)


def test_depends_invalid_dependency():
    def dependency_wo_defaults(arg1, arg2="default_value"):
        pass

    with pytest.raises(TypeError):
        Depends(dependency_wo_defaults)

    with pytest.raises(TypeError):
        Depends(lambda: MagicMock())
