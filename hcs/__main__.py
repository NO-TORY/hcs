#-*- coding: utf-8 -*-

from typing import TYPE_CHECKING, Dict, Any

from jwt import encode, decode
from base64 import b64encode, b64decode

from . import mTranskey
from . import utils
from .hcs import *
from .models import Login, Result

from constants import answer, regionFilter, levelFilter

if TYPE_CHECKING:
    from _typeshed import StrOrBytesPath

def make_token(name, birth, area, school_name, level, password):
    # type: (str, str, str, str, str, str) -> str
    return b64encode(encode({"name": name, "birth": birth, "area": area, "school_name": school_name, "level": level, "password": password}, mTranskey.pubkey).encode()).decode()

def _load_from_token_file(file):
    # type: ("StrOrBytesPath") -> Dict[str, Any]
    return decode(b64decode(open(file, "rb").read()), mTranskey.pubkey, algorithms="HS256")
    
def _load_from_token(token):
    # type: (str) -> Dict[str, Any]
    return decode(b64decode(token), mTranskey.pubkey, algorithms="HS256")

load_from_token = _load_from_token 
load_from_token_file = _load_from_token_file
token_selfcheck = lambda token: selfcheck(**token)

def login(
    name,
    birth,
    area,
    school_name,
    level,
    password,
):
    # type: (str, str, str, str, str, str) -> Login
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

def selfcheck(
    name,
    birth,
    area,
    school_name,
    level,
    password,
    save_token = False,
):
    # type: (str, str, str, str, str, str, bool) -> Result
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

    user_group = utils.selectUserGroup(login_result.atptOfcdcConctUrl, login_result.token)

    userPNo = user_group.userPNo
    token = user_group.token

    user_info = utils.getUserInfo(login_result.atptOfcdcConctUrl, login_result.orgCode, userPNo, token)

    token = user_info.token

    answer["upperToken"] = token
    answer["upperUserNameEncpt"] = name

    registerServey(login_result.atptOfcdcConctUrl, answer)

    if save_token:
        open("token.txt", "w").write(make_token(name, birth, area, school_name, level, password))

    return Result(make_token(name, birth, area, school_name, level, password))
