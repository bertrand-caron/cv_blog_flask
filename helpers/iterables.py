from functools import reduce
from typing import Iterable

def str_merge(args: Iterable[str]) -> str:
    return reduce(
        lambda acc, e: acc + e,
        args,
        '',
    )
