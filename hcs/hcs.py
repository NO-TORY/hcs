#-*- coding: future-annotations -*-

import requests

from typing import Literal, Any

SESSION = requests.Session()

class Route:
    def __init__(self, method: Literal["GET", "POST"], atptOfcdcConctUrl: Any, endpoint: Any = "", **kwargs: Any):
        self.response = SESSION.request(method, atptOfcdcConctUrl + endpoint if "https://" in atptOfcdcConctUrl else "https://" + atptOfcdcConctUrl + endpoint, **kwargs)
        self.response.raise_for_status()

def registerServey(atptOfcdcConctUrl, answer):
    return Route("POST", atptOfcdcConctUrl, "/registerServey", headers={"authorization": answer.get("upperToken"), "content-type": "application/json"}, json=answer)
