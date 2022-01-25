#-*- coding: utf-8 -*-

try:
    from setuptools import setup
except:
    from distutils.core import setup

from io import open
import sys

requirements = [
    "pycryptodome",
    "pyjwt",
    "requests"
]
requirements_extra = {
    "fast": [
        "orjson>=3.5.4"
    ]
}
packages = [
    "hcs",
    "hcs.mTranskey"
]

VERSION_INFO = sys.version_info
VERSION_INFO_TUPLE = (VERSION_INFO.major, VERSION_INFO.minor, VERSION_INFO.micro)

IS_PY2 = VERSION_INFO.major <= 2
IS_PY34 = VERSION_INFO.major == 3 and VERSION_INFO.minor <= 4

if IS_PY2 or IS_PY34:
    requirements.append("future-fstrings")
    requirements.append("typing")

setup(
    name="py-hcs",
    version=open("hcs/version").read(),
    author="노토리",
    description="자가진단 라이브러리.",
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    packages=packages,
    install_requires=requirements,
    extra_requires=requirements_extra,
    include_package_data=True
)
