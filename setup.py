try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import sys, importlib

requirements = ["pycryptodome", "requests", "pyjwt"]
requirements_extra = {
    "fast": [
        "orjson>=3.5.4"
    ]
}
import_checks = ["typing_extensions"]
packages = [
    "hcs",
    "hcs.mTranskey"
]

if sys.version.startswith("2"):
    from distutils.core import setup
    from io import open

def check_imports():
    global import_checks

    for imports in import_checks:
        try:
            importlib.import_module(imports)
        except:
            requirements.append(import_checks)

check_imports()

setup(
    name="py-hcs",
    version=open("hcs/version").read(),
    description="자가진단 라이브러리.",
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    packages=packages,
    install_requires=requirements,
    extra_requires=requirements_extra,
    include_package_data=True
)
