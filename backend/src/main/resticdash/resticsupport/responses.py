from dataclasses_json import dataclass_json, config
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime, timezone

from resticdash.resticdashexception import ResticDashException


# we're backing the timestamp as a string but we want to make sure
# it's always proper ISO8601 and UTC based.
def _grant_iso8601_utc(strvalue: str) -> str:
    try:
        fromiso = datetime.fromisoformat(strvalue)
        return fromiso.astimezone(timezone.utc).isoformat()
    except Exception as ex:
        raise ResticDashException(f"Failed to process date {strvalue} !", ex)


@dataclass_json
@dataclass
class SnapshotInfo:
    """
    The properties match the properties of a single snapshot record for restics json
    """

    id: str
    short_id: str
    time: str = field(metadata=config(encoder=_grant_iso8601_utc, decoder=_grant_iso8601_utc))
    hostname: Optional[str] = None
    username: Optional[str] = None
    uid: Optional[str] = None
    gid: Optional[str] = None
    parent: Optional[str] = None
    tree: Optional[str] = None
    paths: Optional[List[str]] = None

    def __post_init__(self):
        # looks redundant but if we wouldn't do that the time would not be properly adjusted in
        # case this object would be created and thus breaking the invariant that it's always UTC
        self.time = _grant_iso8601_utc(self.time)


@dataclass_json
@dataclass
class BackupInfos:

    name: str
    backup_fail_delay: int
    snapshots: List[SnapshotInfo]
