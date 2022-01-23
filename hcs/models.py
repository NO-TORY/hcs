class FindUser:
    def __init__(self, token):
        self.token = token

class Validate:
    def __init__(self, token):
        self.token = token

class GetUserInfo:
    def __init__(self, token):
        self.token = token

class SearchSchool:
    def __init__(self, atptOfcdcConctUrl, orgCode):
        self.atptOfcdcConctUrl = atptOfcdcConctUrl
        self.orgCode = orgCode

class Login:
    def __init__(self, token, atptOfcdcConctUrl, orgCode):
        self.token = token
        self.atptOfcdcConctUrl = atptOfcdcConctUrl
        self.orgCode = orgCode

class Result:
    def __init__(self, token):
        self.token = token
