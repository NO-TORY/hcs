class FindUser:
    def __init__(self, token):
        self.token = token

class ValidatePassword:
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

class SelectUserGroup:
    def __init__(self, json):
        self.data = {}
        for user in json:
            self.otherYn = user.get("otherYn")
            if self.otherYn == "N":
                self.data = user
                break

        self.token = self.data.get("token")
        self.userPNo = self.data.get("userPNo")

class HasPassword:
    def __init__(self, response):
        if response == "true":
            self.hasPassword = True
        else:
            self.hasPassword = False