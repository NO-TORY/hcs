# -*- coding: euc-kr -*-

from .loader import levels, regions

def levelFilter(word):
    if "유" in word:
        return levels["유등"]

    if "초" in word:
        return levels["초등"]

    if "중" in word:
        return levels["중등"]

    if "특" in word:
        return levels["특수"]

def regionFilter(word):
    if "서울" in word:
        return regions["서울"]

    if "부산" in word:
        return regions["부산"]

    if "대구" in word:
        return regions["대구"]

    if "인천" in word:
        return regions["인천"]

    if "광주" in word:
        return regions["광주"]

    if "대전" in word:
        return regions["대전"]

    if "울산" in word:
        return regions["울산"]

    if "세종" in word:
        return regions["세종"]

    if "경기" in word:
        return regions["경기"]
    
    if "강원" in word:
        return regions["강원"]

    if "충" in word:
        if "북" in word:
            return regions["충북"]

        if "남" in word:
            return regions["충남"]

    if "전" in word:
        if "북" in word:
            return regions["전북"]

        if "남" in word:
            return regions["전남"]

    if "경" in word:
        if "북" in word:
            return regions["경북"]

        if "남" in word:
            return regions["경남"]

    if "제주" in word:
        return regions["제주"]
