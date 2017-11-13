from functools import reduce
from typing import List

def str_merge(args: List[str]) -> str:
    return reduce(
        lambda acc, e: acc + e,
        args,
        '',
    )
