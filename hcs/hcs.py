import requests
from typing import Literal

SESSION = requests.Session()

class Route:
    def __init__(self, method: Literal["GET", "POST"], atptOfcdcConctUrl, endpoint, **kwargs):
        self.response = SESSION.request(method, atptOfcdcConctUrl + endpoint if "https://" in atptOfcdcConctUrl else "https://" + atptOfcdcConctUrl + endpoint, **kwargs)
