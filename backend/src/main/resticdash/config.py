import logging

from dataclasses_json import dataclass_json, config
from dataclasses import dataclass, field
from typing import Optional
from enum import Enum

from resticdash.resticdashexception import ResticDashException


class LogLevel(Enum):
    DEBUG = logging.DEBUG,
    INFO = logging.INFO,
    WARNING = logging.WARNING,
    ERROR = logging.ERROR,


def _loglevel_from_str(value: str) -> LogLevel:
    match value.upper():
        case 'DEBUG': return LogLevel.DEBUG
        case 'INFO': return LogLevel.INFO
        case 'WARNING': return LogLevel.WARNING
        case 'ERROR': return LogLevel.ERROR
        case _: raise ResticDashException(f"'{value}' is not a valid loglevel (DEBUG|INFO|WARNING|ERROR)!")


@dataclass_json
@dataclass
class CfgSettings:

    # Location of the PID file for resticdash
    pidfile: str = '/var/run/resticdash.pid'

    # The log level to use
    log_level: LogLevel = field(default=LogLevel.INFO, metadata=config(
        encoder=lambda v: v.name,
        decoder=_loglevel_from_str
    ))


@dataclass_json
@dataclass
class CfgResticDash:

    settings: Optional[CfgSettings] = None
    version: int = 1

    def __post_init__(self):

        if self.settings is None:
            self.settings = CfgSettings()
