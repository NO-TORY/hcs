from pkgutil import get_data
try:
    from orjson import loads # type: ignore
except:
    from json import loads

from typing import Final

from_path = lambda package, path: get_data(package, path)
json_decode = lambda data: loads(data.decode("utf-8"))

levels = json_decode(from_path("hcs.constants.loader", "levels.json")) # type: Final[dict]
regions = json_decode(from_path("hcs.constants.loader", "regions.json")) # type: Final[dict]
answer = json_decode(from_path("hcs.constants.loader", "answer.json")) # type: dict
