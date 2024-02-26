import os.path
import tempfile

import pytest

from resticdash.resticdashexception import ResticDashException
from resticdash.utils import validation
from resticdash.utils.ioutils import create_temp_file


#@pytest.mark.parametrize("filepath,expected", [
#    ('/tmp/dodobibibabafififofo', "'/tmp/dodobibibabafififofo' must be an existing file !"),
#])

def test_require_file():

    filename = create_temp_file('')

    # 1. file exists
    validation.require_file(filename)

    os.remove(filename)

    # 2. file does not exist
    with pytest.raises(ResticDashException) as exc_info:
        validation.require_file(filename)
    assert str(exc_info.value) == f"'{filename}' must be an existing file !"


def test_require_directory():

    directory = tempfile.mkdtemp()

    # 1. dir exists
    validation.require_directory(directory)

    os.removedirs(directory)

    # 2. dir does not exist
    with pytest.raises(ResticDashException) as exc_info:
        validation.require_directory(directory)
    assert str(exc_info.value) == f"'{directory}' must be a directory !"


def test_require_executable():

    # 1. executable exists on the path
    validation.require_executable("echo")  # TODO: assumption

    # 2. executable doesn't exist
    with pytest.raises(ResticDashException) as exc_info:
        validation.require_executable("krkr123ztzt")
    assert str(exc_info.value) == f"'krkr123ztzt' is not an executable (should be absolute or accessible via the path) !"

    # TODO: to test explicitly provided executables we should provide them


def test_require_not_empty():

    # 1. not empty
    validation.require_not_empty("hello", "value should not be empty")

    # 2. empty
    with pytest.raises(ResticDashException) as exc_info:
        validation.require_not_empty("", "value should not be empty")

    assert str(exc_info.value) == f"value should not be empty"


def test_require_min():

    # 1. minimum is supplied
    validation.require_min(50, 0, "attr")

    # 2. minimum is failed
    with pytest.raises(ResticDashException) as exc_info:
        validation.require_min(50, 60, "attr")

    assert str(exc_info.value) == "The value 50 for attr must be at least greater or equal to 60"
