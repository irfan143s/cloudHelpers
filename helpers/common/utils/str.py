from __future__ import annotations


def is_none_or_empty_str(value: str) -> bool:
    if not value:
        return True
    return False