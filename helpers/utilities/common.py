from __future__ import annotations

def get_lmb_func_event_request(request: dict) -> dict:
    if get_lmb_func_event_source(request) == "lex":
        return request["sessionAttributes"]
    return request


def get_lmb_func_event_source(request: dict) -> str:
    if "bot" in request.keys():
        return "lex"
    return "others"