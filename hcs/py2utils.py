#-*- coding: utf-8 -*-

from json import load
from io import open
from typing import TYPE_CHECKING
from .__main__ import selfcheck
from .models import Result

from sys import version

if not version.startswith("2"):
    raise RuntimeError("This module available for only python 2.")

if TYPE_CHECKING:
    from _typeshed import StrOrBytesPath

def selfcheck_from_json(file):
    # type: ("StrOrBytesPath") -> Result
    """json 파일에서 정보를 불러와 자가진단을 합니다. (파이썬 2 전용)
    
    json 파일 예제: 

    ```json
    {
        "name": "홍길동",
        "birth": "생년월일 6자리",
        "area": "거주 지역",
        "school_name": "학교명",
        "level": "학교 급 (예: 초, 중, 고)",
        "password": "비밀번호",
        "save_token": true "(기본값: false)"
    }
    ```
    """
    return selfcheck(**load(open(file, encoding="utf-8")))
