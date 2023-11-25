from unittest.mock import MagicMock, create_autospec

import pytest
from fastapi import params

from lanarky.adapters.openai.dependencies import Depends
from lanarky.adapters.openai.resources import ChatCompletionResource


def test_depends_success():
    def mock_dependency() -> ChatCompletionResource:
        return create_autospec(ChatCompletionResource)

    dependency = Depends(mock_dependency)
    assert isinstance(dependency, params.Depends)


def test_depends_invalid_dependency():
    def dependency_wo_defaults(arg1, arg2="default_value"):
        pass

    with pytest.raises(TypeError):
        Depends(dependency_wo_defaults)

    with pytest.raises(TypeError):
        Depends(lambda: MagicMock())
