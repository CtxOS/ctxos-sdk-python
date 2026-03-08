#!/usr/bin/env poetry run python

import asyncio

import ctxos
from ctxos import AsyncCtxos


async def main() -> None:
    client = AsyncCtxos()

    res = await client.completions.create(
        model="ctxos-1",
        prompt=f"{ctxos.HUMAN_PROMPT} how does a court case get to the Supreme Court? {ctxos.AI_PROMPT}",
        max_tokens_to_sample=1000,
    )
    print(res.completion)


asyncio.run(main())
