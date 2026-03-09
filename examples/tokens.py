#!/usr/bin/env poetry run python

import asyncio

from ctxos import Ctxos, AsyncCtxos


def sync_tokens() -> None:
    client = Ctxos()

    text = "hello world!"

    tokens = client.tokens.count(input=text)
    print(f"'{text}' is {tokens.tokens} tokens")


async def async_tokens() -> None:
    ctxos = AsyncCtxos()

    text = "first message"
    tokens = await ctxos.tokens.count(input=text)
    print(f"'{text}' is {tokens.tokens} tokens")

    text = "second message"
    tokens = await ctxos.tokens.count(input=text)
    print(f"'{text}' is {tokens.tokens} tokens")


sync_tokens()
asyncio.run(async_tokens())
