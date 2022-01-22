from __future__ import annotations, absolute_import, unicode_literals

from . import mTranskey
from .hcs import *
from .school import *
from .user import *
from json import dumps
import hcs.constants.filter as constant_filters
import hcs.constants.loader as constant_loaders

class LoginResult:
    def __init__(self, token, atptOfcdcConctUrl, orgCode):
        __slots__ = (
            "token",
            "atptOfcdcConctUrl",
            "orgCode"
        )

        self.token = token
        self.atptOfcdcConctUrl = atptOfcdcConctUrl
        self.orgCode = orgCode

def login(
    name: str,
    birth: str,
    area: str,
    school_name: str,
    level: str,
    password: str,
):
    name = mTranskey.encrypt(name)
    birth = mTranskey.encrypt(birth)

    area = constant_filters.regionFilter(area)
    level = constant_filters.levelFilter(level)

    school = SearchSchool(area, level, school_name)
    user = findUser(school.atptOfcdcConctUrl, birth, name, school.orgCode)
    user.response.raise_for_status()
    password_yn = hasPassword(school.atptOfcdcConctUrl, user.response.json()["token"])
    
    if not password_yn:
        raise TypeError("비밀번호가 존재하지 않습니다.")

    mtk = mTranskey.mTransKey("https://hcs.eduro.go.kr/transkeyServlet")
    pw_pad = mtk.new_keypad("number", "password", "password", "password")
    encrypted = pw_pad.encrypt_password(password)
    hm = mtk.hmac_digest(encrypted.encode())
    ps = {
        "raon": [
            {
                "id": "password",
                "enc": encrypted,
                "hmac": hm,
                "keyboardType": "number",
                "keyIndex": mtk.keyIndex,
                "fieldType": "password",
                "seedKey": mtk.crypto.get_encrypted_key(),
                "initTime": mtk.initTime,
                "ExE2E": "false"
            }
        ]
    }

    headers = {
        "authorization": user.response.json()["token"],
        "content-type": "application/json"
    }

    payload = {
        "password": dumps(ps),
        "deviceUuid": "",
        "makeSession": True
    }

    validate = Route("POST", school.atptOfcdcConctUrl, "/v2/validatePassword", headers=headers, json=payload)
    validate.response.raise_for_status()

    return LoginResult(validate.response.json(), school.atptOfcdcConctUrl, school.orgCode)

def selfcheck(
    name: str,
    birth: str,
    area: str,
    school_name: str,
    level: str,
    password: str,
):
    r"""자가진단을 합니다.
    name: str | 자신의 본명
    birth: str | 자신의 생년월일 6자리
    area: str | 자신의 거주 지역
    school_name: str | 자신의 학교 이름
    level: str | 자신의 학교 급 (예: 초, 중, 고, 특)
    password: str | 자신의 자가진단 비밀번호

    ```py
    # 예재 코드
    import hcs

    hcs.selfcheck("홍길동", "060402", "서울", "저기고등학교", "고", "9543")

    """
    login_result = login(name, birth, area, school_name, level, password)

    user_group = SelectUserGroup(login_result.atptOfcdcConctUrl, login_result.token)
    user_group.raise_for_status()
    user_data = {}

    for user in user_group.json():
        if user["otherYn"] == "N":
            user_data = user; break

    userPNo = user_data["userPNo"]
    token = user_data["token"]

    user_info = getUserInfo(login_result.atptOfcdcConctUrl, login_result.orgCode, userPNo, token)
    user_info.raise_for_status()

    token = user_info.json()["token"]

    constant_loaders.answer["upperToken"] = token
    constant_loaders.answer["upperUserNameEncpt"] = name

    servey = Route("POST", login_result.atptOfcdcConctUrl, "/registerServey", headers={"authorization": token, "content-type": "application/json"}, json=constant_loaders.answer)
    return servey