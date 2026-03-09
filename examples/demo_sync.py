#!/usr/bin/env poetry run python

from ctxos import Ctxos


def main() -> None:
    client = Ctxos()

    res = client.complete.create(
        model="ctxos-1",
        prompt="how does a court case get to the Supreme Court?",
        max_tokens=1000,
    )
    print(res.choices[0].text)  # type: ignore[index]


main()
