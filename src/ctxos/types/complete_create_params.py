# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union
from typing_extensions import Required, TypedDict

from .tool import Tool, ToolChoice

__all__ = ["CompleteCreateParams"]


class CompleteCreateParams(TypedDict, total=False):
    model: Required[str]

    prompt: Required[str]

    max_tokens: int

    temperature: float

    tools: List[Tool]

    tool_choice: Union[str, ToolChoice]
