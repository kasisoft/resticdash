from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class CfgSettings:

    # Location of the PID file for resticdash
    pidfile: str = '/var/run/resticdash.pid'


@dataclass_json
@dataclass
class CfgResticDash:

    settings: Optional[CfgSettings] = None
    version: int = 1

    def __post_init__(self):

        if self.settings is None:
            self.settings = CfgSettings()
