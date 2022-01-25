from __future__ import annotations

import requests

try:
    from typing import Literal, TYPE_CHECKING, Any
except:
    from typing_extensions import Literal, TYPE_CHECKING, Any

if TYPE_CHECKING:
    from _typeshed import Self

SESSION = requests.Session()

class Route:
    def __init__(self, method, atptOfcdcConctUrl, endpoint, **kwargs):
        # type: (Self, Literal["GET", "POST"], Any, str, Any) -> None
        self.response = SESSION.request(method, atptOfcdcConctUrl + endpoint if "https://" in atptOfcdcConctUrl else "https://" + atptOfcdcConctUrl + endpoint, **kwargs)
        self.response.raise_for_status()
