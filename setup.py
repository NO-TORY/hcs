from setuptools import setup, find_packages
from contextlib import closing

requirements = ["pycryptodome", "requests", "pyjwt"]

with closing(open("hcs/version")) as f:
    version = f.read()

setup(
    name="py-hcs",
    version=version,
    description="자가진단 라이브러리.",
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True
)
