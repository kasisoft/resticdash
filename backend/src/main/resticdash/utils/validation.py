import os

from resticdash.resticdashexception import ResticDashException


def require_non_existence(filepath: str):
    if os.path.exists(filepath):
        raise ResticDashException(f"Found '{filepath}'. Make sure to shutdown a potentially running instance !")


def require_file(filepath: str):
    if not os.path.isfile(filepath):
        raise ResticDashException(f"'{filepath}' must be an existing file !")


def require_directory(filepath: str):
    if not os.path.isdir(filepath):
        raise ResticDashException(f"'{filepath}' must be a directory !")


def require_not_empty(obj, msg: str):
    if (obj is None) or (len(obj) == 0):
        raise ResticDashException(msg)
