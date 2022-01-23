from .hcs import Route
from .models import FindUser, GetUserInfo

def findUser(atptOfcdcConctUrl, birthday: str, name: str, orgCode: str, loginType: str = "school", stdntPNo = None):
    payload = {
        "birthday": birthday,
        "loginType": loginType,
        "name": name,
        "orgCode": orgCode,
        "stdntPNo": stdntPNo
    }

    return FindUser(Route("POST", atptOfcdcConctUrl, "/v2/findUser", json=payload).response.json().get("token"))

def hasPassword(atptOfcdcConctUrl, token: str):
    response = Route("POST", atptOfcdcConctUrl, "/v2/hasPassword", headers={"authorization": token, "content-type": "application/json"}, json={})
    if response.response.text == "true":
        return True
    else:
        return False

def SelectUserGroup(atptOfcdcConctUrl, token: str):
    return Route("POST", atptOfcdcConctUrl, "/v2/selectUserGroup", headers={"Authorization": token, "content-type": "application/json", "X-Requested-With": "XMLHttpRequest"}, json={}).response

def getUserInfo(atptOfcdcConctUrl, orgCode: str, userPNo: str, token: str):
    return GetUserInfo(Route("POST", atptOfcdcConctUrl, "/v2/getUserInfo", headers={"authorization": token, "content-type": "application/json"}, json=dict(orgCode=orgCode, userPNo=userPNo)).response.json().get("token"))
