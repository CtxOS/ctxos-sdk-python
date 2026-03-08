#!/usr/bin/env poetry run python

import ctxos
from ctxos import Ctxos


def main() -> None:
    client = Ctxos()

    res = client.completions.create(
        model="ctxos-1",
        prompt=f"{ctxos.HUMAN_PROMPT} how does a court case get to the Supreme Court? {ctxos.AI_PROMPT}",
        max_tokens_to_sample=1000,
    )
    print(res.completion)


main()
