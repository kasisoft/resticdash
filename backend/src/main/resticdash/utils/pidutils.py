import os

from typing import Optional

from resticdash.utils import ioutils, validation


class PidHandler:
    """
    Generate a PID file for the current process and cleans it up when exiting.
    """

    def __init__(self, pidfile):
        self._pidfile = pidfile

    @staticmethod
    def read_pid(pidfile) -> Optional[int]:
        if os.path.isfile(pidfile):
            with open(pidfile, 'r') as file:
                return int(file.read())
        return None

    def __enter__(self):
        validation.require_non_existence(self._pidfile)
        with open(self._pidfile, 'w') as file:
            file.write(str(os.getpid()))

    def __exit__(self, exc_type, exc_val, exc_tb):
        ioutils.remove_files([self._pidfile])



