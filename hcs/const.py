from .constants.loader import from_path

__version__ = from_path("hcs", "version").decode()
