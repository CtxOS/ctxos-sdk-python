# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["TokenCountResponse"]


class TokenCountResponse(BaseModel):
    tokens: Optional[int] = None
