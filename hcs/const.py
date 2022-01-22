from pkgutil import get_data

__version__ = get_data("hcs", "version").decode()