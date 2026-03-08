# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["CompleteCreateResponse", "Choice", "Usage"]


class Choice(BaseModel):
    finish_reason: Optional[str] = None

    index: Optional[int] = None

    text: Optional[str] = None


class Usage(BaseModel):
    completion_tokens: Optional[int] = None

    prompt_tokens: Optional[int] = None

    total_tokens: Optional[int] = None


class CompleteCreateResponse(BaseModel):
    id: Optional[str] = None

    choices: Optional[List[Choice]] = None

    model: Optional[str] = None

    object: Optional[str] = None

    usage: Optional[Usage] = None
