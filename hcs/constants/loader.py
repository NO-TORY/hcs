from pkgutil import get_data
from json import loads
from typing import Final

from_path = lambda package, path: get_data(package, path)
json_decode = lambda data: loads(data.decode())

levels: Final[dict] = json_decode(from_path("hcs.constants.loader", "levels.json"))
regions: Final[dict] = json_decode(from_path("hcs.constants.loader", "regions.json"))
answer: dict = json_decode(from_path("hcs.constants.loader", "answer.json"))
