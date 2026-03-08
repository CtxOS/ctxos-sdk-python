#!/usr/bin/env poetry run python

import asyncio

from ctxos import Ctxos, AsyncCtxos


def sync_tokens() -> None:
    client = Ctxos()

    text = "hello world!"

    tokens = client.count_tokens(text)
    print(f"'{text}' is {tokens} tokens")

    assert tokens == 3


async def async_tokens() -> None:
    ctxos = AsyncCtxos()

    text = "fist message"
    tokens = await ctxos.count_tokens(text)
    print(f"'{text}' is {tokens} tokens")

    text = "second message"
    tokens = await ctxos.count_tokens(text)
    print(f"'{text}' is {tokens} tokens")


sync_tokens()
asyncio.run(async_tokens())
