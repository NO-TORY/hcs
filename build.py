import os

os.system("pip install twine")
os.system("python setup.py sdist")
os.system("python -m twine upload dist/*")
