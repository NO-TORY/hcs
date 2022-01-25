fast = True

try:
    from orjson import dumps # type: ignore
except:
    from json import dumps

    fast = False

from jwt import encode, decode
from base64 import b64encode, b64decode

from . import mTranskey
from .hcs import *
from .school import *
from .user import *
from .models import Validate, Login, Result

import hcs.constants.filter as constant_filters
import hcs.constants.loader as constant_loaders

from sys import version

if version.startswith("2"):
    from io import open

make_token = lambda name, birth, area, school_name, level, password: b64encode(encode({"name": name, "birth": birth, "area": area, "school_name": school_name, "level": level, "password": password}, mTranskey.pubkey).encode()).decode()
load_from_token_file = lambda file: decode(b64decode(open(file).read()), mTranskey.pubkey, algorithms="HS256")
load_from_token = lambda token: decode(b64decode(token), mTranskey.pubkey, algorithms="HS256")
token_selfcheck = lambda token: selfcheck(**load_from_token(token))

def login(
    name,
    birth,
    area,
    school_name,
    level,
    password,
):
    name = mTranskey.encrypt(name)
    birth = mTranskey.encrypt(birth)

    area = constant_filters.regionFilter(area)
    level = constant_filters.levelFilter(level)

    school = searchSchool(area, level, school_name)
    user = findUser(school.atptOfcdcConctUrl, birth, name, school.orgCode)
    password_yn = hasPassword(school.atptOfcdcConctUrl, user.token)
    
    assert password_yn == True, "비밀번호가 설정되지 않았습니다."

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
        "authorization": user.token,
        "content-type": "application/json"
    }

    payload = {
        "password": dumps(ps).decode() if fast else dumps(ps),
        "deviceUuid": "",
        "makeSession": True
    }

    validate = Route("POST", school.atptOfcdcConctUrl, "/v2/validatePassword", headers=headers, json=payload)
    token = validate.response.json()
    validate = Validate(token)
    return Login(validate.token, school.atptOfcdcConctUrl, school.orgCode)

def selfcheck(
    name,
    birth,
    area,
    school_name,
    level,
    password,
    save_token = False,
):
    r"""자가진단을 합니다.
    name: str | 자신의 본명
    birth: str | 자신의 생년월일 6자리
    area: str | 자신의 거주 지역
    school_name: str | 자신의 학교 이름
    level: str | 자신의 학교 급 (예: 초, 중, 고, 특)
    password: str | 자신의 자가진단 비밀번호
    save_token: bool | 토큰 저장 여부입니다. 토큰은 token.txt로 저장됩니다.

    ```py
    # 예재 코드
    import hcs

    hcs.selfcheck("홍길동", "060402", "서울", "저기고등학교", "고", "9543")
    ```
    """
    login_result = login(name, birth, area, school_name, level, password)

    user_group = SelectUserGroup(login_result.atptOfcdcConctUrl, login_result.token)
    user_data = {}

    for user in user_group.json():
        if user["otherYn"] == "N":
            user_data = user
            break

    userPNo = user_data["userPNo"]
    token = user_data["token"]

    user_info = getUserInfo(login_result.atptOfcdcConctUrl, login_result.orgCode, userPNo, token)

    token = user_info.token

    constant_loaders.answer["upperToken"] = token
    constant_loaders.answer["upperUserNameEncpt"] = name

    Route("POST", login_result.atptOfcdcConctUrl, "/registerServey", headers={"authorization": token, "content-type": "application/json"}, json=constant_loaders.answer)

    if save_token:
        open("token.txt", "w").write(make_token(name, birth, area, school_name, level, password))

    return Result(make_token(name, birth, area, school_name, level, password))
