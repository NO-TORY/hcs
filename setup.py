from setuptools import setup
from contextlib import closing

packages = ["hcs"]
requirements = ["pycryptodome", "requests"]

with closing(open("hcs/version")) as f:
    version = f.read()

setup(
    name="py-hcs",
    version=version,
    description="자가진단 라이브러리.",
    packages=packages,
    install_requires=requirements,
    include_package_data=True
)
