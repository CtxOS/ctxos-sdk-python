# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import List, Union

import httpx

from ..types import complete_create_params
from .._types import Body, Omit, Query, Headers, NotGiven, omit, not_given
from .._utils import maybe_transform, async_maybe_transform
from .._compat import cached_property
from .._resource import SyncAPIResource, AsyncAPIResource
from .._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..types.tool import Tool, ToolChoice
from .._base_client import make_request_options
from ..types.complete_create_response import CompleteCreateResponse

__all__ = ["CompleteResource", "AsyncCompleteResource"]


class CompleteResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> CompleteResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CtxOS/ctxos-sdk-python#accessing-raw-response-data-eg-headers
        """
        return CompleteResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> CompleteResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CtxOS/ctxos-sdk-python#with_streaming_response
        """
        return CompleteResourceWithStreamingResponse(self)

    def create(
        self,
        *,
        model: str,
        prompt: str,
        max_tokens: int | Omit = omit,
        temperature: float | Omit = omit,
        tools: List[Tool] | Omit = omit,
        tool_choice: Union[str, ToolChoice] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompleteCreateResponse:
        """
        Create completion

        Args:
          tools: A list of tools the model may call. The model will determine which (if any) function to call.

          tool_choice: Controls which (if any) function is called by the model. Can be "none", "auto", or a specific function name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return self._post(
            "/v1/complete",
            body=maybe_transform(
                {
                    "model": model,
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "tools": tools,
                    "tool_choice": tool_choice,
                },
                complete_create_params.CompleteCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompleteCreateResponse,
        )


class AsyncCompleteResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncCompleteResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/CtxOS/ctxos-sdk-python#accessing-raw-response-data-eg-headers
        """
        return AsyncCompleteResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncCompleteResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/CtxOS/ctxos-sdk-python#with_streaming_response
        """
        return AsyncCompleteResourceWithStreamingResponse(self)

    async def create(
        self,
        *,
        model: str,
        prompt: str,
        max_tokens: int | Omit = omit,
        temperature: float | Omit = omit,
        tools: List[Tool] | Omit = omit,
        tool_choice: Union[str, ToolChoice] | Omit = omit,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = not_given,
    ) -> CompleteCreateResponse:
        """
        Create completion

        Args:
          tools: A list of tools the model may call. The model will determine which (if any) function to call.

          tool_choice: Controls which (if any) function is called by the model. Can be "none", "auto", or a specific function name.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        return await self._post(
            "/v1/complete",
            body=await async_maybe_transform(
                {
                    "model": model,
                    "prompt": prompt,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "tools": tools,
                    "tool_choice": tool_choice,
                },
                complete_create_params.CompleteCreateParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=CompleteCreateResponse,
        )


class CompleteResourceWithRawResponse:
    def __init__(self, complete: CompleteResource) -> None:
        self._complete = complete

        self.create = to_raw_response_wrapper(
            complete.create,
        )


class AsyncCompleteResourceWithRawResponse:
    def __init__(self, complete: AsyncCompleteResource) -> None:
        self._complete = complete

        self.create = async_to_raw_response_wrapper(
            complete.create,
        )


class CompleteResourceWithStreamingResponse:
    def __init__(self, complete: CompleteResource) -> None:
        self._complete = complete

        self.create = to_streamed_response_wrapper(
            complete.create,
        )


class AsyncCompleteResourceWithStreamingResponse:
    def __init__(self, complete: AsyncCompleteResource) -> None:
        self._complete = complete

        self.create = async_to_streamed_response_wrapper(
            complete.create,
        )
