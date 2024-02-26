import os

from resticdash.resticdashexception import ResticDashException


def require_non_existence(filepath: str):
    if os.path.exists(filepath):
        raise ResticDashException(f"Found '{filepath}'. Make sure to shutdown a potentially running instance !")


def require_file(filepath: str):
    if not os.path.isfile(filepath):
        raise ResticDashException(f"'{filepath}' must be an existing file !")

