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
    return selfcheck(**load(open(file, encoding="utf-8")))
