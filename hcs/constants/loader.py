from pkgutil import get_data
from json import loads
try:
    from typing import Final
except:
    from typing_extensions import Final

from_path = lambda package, path: get_data(package, path)
json_decode = lambda data: loads(data.decode())

levels = json_decode(from_path("hcs.constants.loader", "levels.json")) # type: Final[dict]
regions = json_decode(from_path("hcs.constants.loader", "regions.json")) # type: Final[dict]
answer = json_decode(from_path("hcs.constants.loader", "answer.json")) # type: dict
