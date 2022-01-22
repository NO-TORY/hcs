from .loader import levels, regions

import re

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
    region = ",".join(regions)

    word = re.search(word, region).group()

    return regions[re.sub(fr"[^{word}]", "", region)]

