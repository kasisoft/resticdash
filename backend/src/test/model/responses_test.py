import pytest

from resticdash.resticdashexception import ResticDashException
from resticdash.resticsupport.responses import SnapshotInfo


def test_iso8601_utc():

    # verifies that the time is stored utc based
    backup_info = SnapshotInfo("dodo", "bibo", "2024-01-04T19:56:37.055386+01:00", "hostname", "username", "uid", "gid")
    assert str(backup_info.time) == "2024-01-04T18:56:37.055386+00:00"


def test_invalid_iso8601():

    with pytest.raises(ResticDashException) as exc_info:
        SnapshotInfo("dodo", "bibo", "bodo mcfrunkel", "hostname", "username", "uid", "gid")
    assert str(exc_info.value) == ("Failed to process date bodo mcfrunkel !: "
                                   "(Cause: Invalid isoformat string: 'bodo mcfrunkel')")
