# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from ctxos import Ctxos, AsyncCtxos
from ctxos.types import CompleteCreateResponse
from tests.utils import assert_matches_type

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestComplete:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create(self, client: Ctxos) -> None:
        complete = client.complete.create(
            model="ctxos-1",
            prompt="prompt",
        )
        assert_matches_type(CompleteCreateResponse, complete, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_method_create_with_all_params(self, client: Ctxos) -> None:
        complete = client.complete.create(
            model="ctxos-1",
            prompt="prompt",
            max_tokens=0,
            temperature=0,
        )
        assert_matches_type(CompleteCreateResponse, complete, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_raw_response_create(self, client: Ctxos) -> None:
        response = client.complete.with_raw_response.create(
            model="ctxos-1",
            prompt="prompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        complete = response.parse()
        assert_matches_type(CompleteCreateResponse, complete, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    def test_streaming_response_create(self, client: Ctxos) -> None:
        with client.complete.with_streaming_response.create(
            model="ctxos-1",
            prompt="prompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            complete = response.parse()
            assert_matches_type(CompleteCreateResponse, complete, path=["response"])

        assert cast(Any, response.is_closed) is True


class TestAsyncComplete:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create(self, async_client: AsyncCtxos) -> None:
        complete = await async_client.complete.create(
            model="ctxos-1",
            prompt="prompt",
        )
        assert_matches_type(CompleteCreateResponse, complete, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_method_create_with_all_params(self, async_client: AsyncCtxos) -> None:
        complete = await async_client.complete.create(
            model="ctxos-1",
            prompt="prompt",
            max_tokens=0,
            temperature=0,
        )
        assert_matches_type(CompleteCreateResponse, complete, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_raw_response_create(self, async_client: AsyncCtxos) -> None:
        response = await async_client.complete.with_raw_response.create(
            model="ctxos-1",
            prompt="prompt",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        complete = await response.parse()
        assert_matches_type(CompleteCreateResponse, complete, path=["response"])

    @pytest.mark.skip(reason="Mock server tests are disabled")
    @parametrize
    async def test_streaming_response_create(self, async_client: AsyncCtxos) -> None:
        async with async_client.complete.with_streaming_response.create(
            model="ctxos-1",
            prompt="prompt",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            complete = await response.parse()
            assert_matches_type(CompleteCreateResponse, complete, path=["response"])

        assert cast(Any, response.is_closed) is True
