from .__main__ import (
    selfcheck,
    token_selfcheck,
    load_from_token,
    load_from_token_file,
)
from .const import __version__
from sys import version

if int(version[0]) <= 2:
    from . import constants
