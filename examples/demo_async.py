#!/usr/bin/env poetry run python

import asyncio

from ctxos import AsyncCtxos


async def main() -> None:
    client = AsyncCtxos()

    res = await client.complete.create(
        model="ctxos-1",
        prompt="how does a court case get to the Supreme Court?",
        max_tokens=1000,
    )
    print(res.choices[0].text)  # type: ignore[index]


asyncio.run(main())
