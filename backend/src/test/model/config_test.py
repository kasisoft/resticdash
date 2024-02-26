import tempfile
import pytest

from resticdash.config import CfgResticDash, CfgBackup, CfgSettings
from resticdash.resticdashexception import ResticDashException


def test_invalid_directory():
    with pytest.raises(ResticDashException) as exc_info:
        cfg = CfgResticDash(None, {"bridget": CfgBackup("abcd", "/tmp/dodo")})
    assert str(exc_info.value) == "'/tmp/dodo' must be a directory !"


def test_invalid_restic_directory():
    directory = tempfile.mktemp()
    # locksdir = os.path.join(directory, "locks")
    with pytest.raises(ResticDashException) as exc_info:
        cfg = CfgResticDash(None, {"bridget": CfgBackup("abcd", directory)})
    assert str(exc_info.value) == f"'{directory}' must be a directory !"


def test_no_backups():
    with pytest.raises(ResticDashException) as exc_info:
        cfg = CfgResticDash(None, {})
    assert str(exc_info.value) == "There must be at least one backup declaration !"


def test_invalid_delay():
    with pytest.raises(ResticDashException) as exc_info:
        cfg = CfgResticDash(CfgSettings(delay = 59), {})
    assert str(exc_info.value) == "The value 59 for delay must be at least greater or equal to 60"


def test_invalid_executable():
    with pytest.raises(ResticDashException) as exc_info:
        cfg = CfgResticDash(CfgSettings(restic = "froppel"), {})
    assert str(exc_info.value) == "'froppel' is not an executable (should be absolute or accessible via the path) !"
