#-*- coding: utf-8 -*-

try:
    from setuptools import setup
except:
    from distutils.core import setup

from io import open

requirements = open("requirements.txt", encoding="utf-8").read().splitlines()

requirements_extra = {
    "fast": [
        "orjson>=3.5.4"
    ]
}

packages = [
    "hcs",
    "hcs.mTranskey"
]

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
    include_package_data=True,
    python_requires=">=3"
)
