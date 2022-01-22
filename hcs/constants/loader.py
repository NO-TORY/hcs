from pkgutil import get_data
from json import loads
from typing import Final

levels: Final[dict] = loads(get_data("hcs.constants.loader", "levels.json").decode("utf-8"))
regions: Final[dict] = loads(get_data("hcs.constants.loader", "regions.json").decode("utf-8"))
answer: dict = loads(get_data("hcs.constants.loader", "answer.json").decode("utf-8"))