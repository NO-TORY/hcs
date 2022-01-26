#-*- coding: future-fstrings -*-

from .hcs import Route
from .models import *

fast = True

try:
    from orjson import dumps # type: ignore
except:
    from json import dumps
    fast = False

def searchSchool(lctnScCode, schulCrseScCode, orgName, loginType = "school"):
    response = Route("GET", "https://hcs.eduro.go.kr", f"/v2/searchSchool?lctnScCode={lctnScCode}&schulCrseScCode={schulCrseScCode}&orgName={orgName}&loginType={loginType}")
        
    if len(response.response.json()["schulList"]) > 1:
        raise IndexError("너무 많은 학교가 검색 되었습니다.")

    school = response.response.json()["schulList"][0]
    orgCode = school.get("orgCode")
    atptOfcdcConctUrl = school.get("atptOfcdcConctUrl")

    return SearchSchool(atptOfcdcConctUrl, orgCode)

def findUser(atptOfcdcConctUrl, birthday, name, orgCode):
    payload = {
        "birthday": birthday,
        "name": name,
        "orgCode": orgCode,
        "loginType": "school",
        "stdntPNo": None
    }

    response = Route("POST", atptOfcdcConctUrl, "/v2/findUser", json=payload)
    return FindUser(response.response.json().get("token"))

def hasPassword(atptOfcdcConctUrl, token):
    headers = {
        "authorization": token,
        "content-type": "application/json"
    }

    payload = {}

    response = Route("POST", atptOfcdcConctUrl, "/v2/hasPassword", headers=headers, json=payload)
    return HasPassword(response.response.text).hasPassword

def selectUserGroup(atptOfcdcConctUrl, token):
    headers = {
        "authorization": token,
        "content-type": "application/json",
        "X-Requested-With": "XMLHttpRequest"
    }

    payload = {}
    
    response = Route("POST", atptOfcdcConctUrl, "/v2/selectUserGroup", headers=headers, json=payload)
    return SelectUserGroup(response.response.json())

def getUserInfo(atptOfcdcConctUrl, orgCode, userPNo, token):
    headers = {
        "authorization": token,
        "content-type": "application/json"
    }

    payload = {
        "orgCode": orgCode,
        "userPNo": userPNo
    }

    response = Route("POST", atptOfcdcConctUrl, "/v2/getUserInfo", headers=headers, json=payload)
    return GetUserInfo(response.response.json().get("token"))

def validatePassword(atptOfcdcConctUrl, enc, hmac, keyIndex, seedKey, initTime, token):
    password = {
        "raon": [
            {
                "id": "password",
                "enc": enc,
                "hmac": hmac,
                "keyboardType": "number",
                "keyIndex": keyIndex,
                "fieldType": "password",
                "seedKey": seedKey,
                "initTime": initTime,
                "ExE2E": "false"
            }
        ]
    }

    headers = {
        "authorization": token,
        "content-type": "application/json"
    }

    payload = {
        "password": dumps(password).decode() if fast else dumps(password),
        "deviceUuid": "",
        "makeSession": True
    }

    response = Route("POST", atptOfcdcConctUrl, "/v2/validatePassword", headers=headers, json=payload)
    return ValidatePassword(response.response.json())
