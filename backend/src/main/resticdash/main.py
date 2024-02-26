import logging
import signal
import sys
import os

from typing import Optional, List
from setproctitle import setproctitle

from resticdash.utils.ioutils import load_yaml, grant_password_file, remove_files
from resticdash.config import CfgResticDash
from resticdash.getargs import get_args
from resticdash.resticsupport.backupmanager import BackupManager
from resticdash.utils.pidutils import PidHandler

NAME = "resticdash"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    datefmt="%H:%M:%S"
)

logger = logging.getLogger(NAME)

backupmanager: Optional[BackupManager] = None
removable_password_files: List[str] = []
configuration: Optional[CfgResticDash] = None


def _load_configuration(configuration_file) -> tuple[Optional[CfgResticDash], list[str]]:
    result = load_yaml(CfgResticDash, configuration_file, True)
    to_remove: list[str] = []
    if result is not None:
        for backup in result.backups.values():
            backup.password, created = grant_password_file(backup.password)
            if created:
                to_remove.append(backup.password)
    return result, to_remove


def _shutdown(signal, frame):

    global removable_password_files
    global backupmanager

    logger.info("Shutting down...")

    if len(removable_password_files) > 0:
        try:
            remove_files(removable_password_files)
        except Exception as ex:
            logger.error("Failed to delete all password files", exc_info=ex)
        removable_password_files = []

    if backupmanager is not None:
        try:
            backupmanager.stop()
        except Exception as ex:
            logger.error("Failed to stop the BackupManager", exc_info=ex)
        backupmanager = None

    logger.info("... completed shutdown")


def _kill():

    pid = PidHandler.read_pid(configuration.settings.pidfile)
    if pid is not None:
        logger.info(f"Sending SIGINT to {pid}")
        os.kill(pid, signal.SIGINT)
    logger.info("Done")


def _resticdash():

    global backupmanager

    backupmanager = BackupManager(configuration)
    backupmanager.start()
    backupmanager.join(600)   # stay alive for 10 min
    _shutdown(None, None)


def main():

    global removable_password_files
    global configuration

    config_file, kill = get_args()

    configuration, removable_password_files = _load_configuration(config_file)
    logging.basicConfig(level = configuration.settings.log_level.value[0])
    logger.setLevel(configuration.settings.log_level.value[0])

    if kill:
        _kill()
        return

    with PidHandler(configuration.settings.pidfile):
        _resticdash()


if __name__ == '__main__':
    try:
        setproctitle(NAME)
        signal.signal(signal.SIGINT, _shutdown)
        main()
    except Exception as ex:
        logger.error(f"{NAME} failed", exc_info=ex)
        sys.exit(1)
