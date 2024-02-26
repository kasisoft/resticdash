import os
from resticdash.resticdashexception import ResticDashException


def require_file(filepath: str):
    if not os.path.isfile(filepath):
        raise ResticDashException(f"'{filepath}' must be an existing file !")

