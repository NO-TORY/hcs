#-*- coding: future-annotations -*-

import jwt, base64

from . import mTranskey
from . import utils
from .hcs import *
from .models import Login, Result

from .constants import answer, regionFilter, levelFilter

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from _typeshed import StrOrBytesPath

class Token:
    def __init__(
        self,
        name: Any,
        birth: Any,
        area: Any,
        school_name: Any,
        level: Any,
        password: Any
    ):
        self.payload = {
            "name": name,
            "birth": birth,
            "area": area,
            "school_name": school_name,
            "level": level,
            "password": password
        }

    def make_token(self):
        return base64.b64encode(
            jwt.encode(self.payload, mTranskey.pubkey).encode()
        ).decode()

    @staticmethod
    def load_from_token(token):
        if isinstance(token, bytes):
            return jwt.decode(
                base64.b64decode(token),
                mTranskey.pubkey,
                algorithms="HS256"
            )
        else:
            return jwt.decode(
                base64.decode(token.encode()),
                mTranskey.pubkey,
                algorithms="HS256"
            )

    @classmethod
    def load_from_file(cls, file: "StrOrBytesPath"):
        with open(file, "rb") as f:
            return cls.load_from_token(f.read())

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
    area = regionFilter(area)
    level = levelFilter(level)
    school = utils.searchSchool(area, level, school_name)
    user = utils.findUser(school.atptOfcdcConctUrl, birth, name, school.orgCode)
    password_yn = utils.hasPassword(school.atptOfcdcConctUrl, user.token)

    assert password_yn == True, "비밀번호가 설정되지 않았습니다."

    transKey = mTranskey.mTransKey("https://hcs.eduro.go.kr/transkeyServlet")
    pad = transKey.new_keypad("number", "password", "password", "password")
    encrypted = pad.encrypt_password(password)
    hmac = transKey.hmac_digest(encrypted.encode())
    
    validate = utils.validatePassword(
        school.atptOfcdcConctUrl,
        encrypted,
        hmac,
        transKey.keyIndex,
        transKey.crypto.get_encrypted_key(),
        transKey.initTime,
        user.token
    )

    return Login(validate.token, school.atptOfcdcConctUrl, school.orgCode)

def token_selfcheck(token: Any) -> None:
    return selfcheck(**Token.load_from_token(token))

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
    ```
    """
    login_result = login(name, birth, area, school_name, level, password)

    user_group = utils.selectUserGroup(login_result.atptOfcdcConctUrl, login_result.token)

    userPNo = user_group.userPNo
    token = user_group.token

    user_info = utils.getUserInfo(login_result.atptOfcdcConctUrl, login_result.orgCode, userPNo, token)

    token = user_info.token

    answer["upperToken"] = token
    answer["upperUserNameEncpt"] = name

    registerServey(login_result.atptOfcdcConctUrl, answer)

    return Result(Token(name, birth, area, school_name, level, password).make_token())
