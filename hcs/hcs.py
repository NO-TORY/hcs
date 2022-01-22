import requests

SESSION = requests.Session()

class Route:
    def __init__(self, method, atptOfcdcConctUrl, endpoint, **kwargs):
        global SESSION

        self.response = SESSION.request(method, atptOfcdcConctUrl + endpoint if "https://" in atptOfcdcConctUrl else "https://" + atptOfcdcConctUrl + endpoint, **kwargs)