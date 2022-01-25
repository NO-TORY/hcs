#-*- coding: utf-8 -*-

from .__main__ import (
    selfcheck,
    token_selfcheck,
    load_from_token,
    load_from_token_file,
)
from .const import __version__
from . import constants
from sys import version

if version.startswith("2"):
    from .py2utils import selfcheck_from_json
