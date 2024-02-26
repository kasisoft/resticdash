import logging
import os

from dataclasses_json import dataclass_json, config
from dataclasses import dataclass, field
from typing import Optional, Dict, List
from enum import Enum

from resticdash.resticdashexception import ResticDashException
from resticdash.utils import validation


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
class CfgBackup:

    # Either the password or the location of a file that contains the password.
    password: str

    # The directory for the repository
    repository: str

    # The time delay in seconds after which a backup should have occured. By default the globally configured value.
    backup_fail_delay: Optional[int] = None

    def __post_init__(self):
        validation.require_directory(self.repository)
        validation.require_directory(os.path.join(self.repository, 'locks'))


@dataclass_json
@dataclass
class CfgSettings:

    # The location within the filesystem of the restic executable or the name of the executable on the path.
    restic: str = 'restic'

    # The time delay in seconds to wait until the backup information will be updated
    delay: int = 600  # 10min

    # The time delay in seconds after which a backup should have occured
    backup_fail_delay: int = 86400  # 1 day

    # A list of allowed origins
    origins: Optional[List[str]] = None

    # The context path for the deployment
    context_path: str = ''

    # The port to use serving the content
    port: int = 8080

    # Location of the PID file for resticdash
    pidfile: str = '/var/run/resticdash.pid'

    # The log level to use
    log_level: LogLevel = field(default=LogLevel.INFO, metadata=config(
        encoder=lambda v: v.name,
        decoder=_loglevel_from_str
    ))

    def __post_init__(self):
        if self.context_path == '/':
            self.context_path = ''
        elif len(self.context_path) > 1:
            if self.context_path[-1] == '/':
                self.context_path = self.context_path[:-1]
            if self.context_path[0] != '/':
                self.context_path = '/' + self.context_path
        if self.origins is None:
            self.origins = []
        validation.require_min(self.delay, 60, 'delay')
        validation.require_min(self.backup_fail_delay, 60, 'backup_fail_delay')
        validation.require_executable(self.restic)


@dataclass_json
@dataclass
class CfgResticDash:

    backups: Dict[str, CfgBackup] = field(default_factory=dict)
    settings: Optional[CfgSettings] = None
    version: int = 1

    def __post_init__(self):

        if self.settings is None:
            self.settings = CfgSettings()

        validation.require_not_empty(self.backups, "There must be at least one backup declaration !")

        for cfg_backup in self.backups.values():
            if cfg_backup.backup_fail_delay is None:
                cfg_backup.backup_fail_delay = self.settings.backup_fail_delay

