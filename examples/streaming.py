#!/usr/bin/env poetry run python

import asyncio

from ctxos import Ctxos, AsyncCtxos, APIStatusError

client = Ctxos()
async_client = AsyncCtxos()

question = """
Hey Ctxos! How can I recursively list all files in a directory in Python?
"""


def sync_request() -> None:
    response = client.complete.create(
        prompt=question,
        model="ctxos-1",
        max_tokens=300,
    )
    print(response.choices[0].text)  # type: ignore[index]


async def async_request() -> None:
    response = await async_client.complete.create(
        prompt=question,
        model="ctxos-1",
        max_tokens=300,
    )
    print(response.choices[0].text)  # type: ignore[index]


def request_error() -> None:
    try:
        client.complete.create(
            prompt=question,
            model="Ctxos-unknown-model",
            max_tokens=300,
        )
    except APIStatusError as err:
        print(f"Caught API status error with response body: {err.response.text}")


sync_request()
asyncio.run(async_request())
request_error()
