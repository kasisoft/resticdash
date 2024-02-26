import logging
import signal
import sys
import os

from typing import Optional, List
from flask import Blueprint, send_from_directory
from setproctitle import setproctitle

from resticdash.utils.ioutils import load_yaml, grant_password_file, remove_files
from resticdash.config import CfgResticDash
from resticdash.getargs import get_args
from resticdash.resticsupport.backupmanager import BackupManager
from resticdash.stoppableflask import StoppableFlask
from resticdash.utils.pidutils import PidHandler

NAME = "resticdash"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    datefmt="%H:%M:%S"
)

logger = logging.getLogger(NAME)

backupmanager: Optional[BackupManager] = None
flaskthread: Optional[StoppableFlask] = None
removable_password_files: List[str] = []
configuration: Optional[CfgResticDash] = None


def view_get_frontend_config():
    return configuration.frontend.to_dict()


def view_get_restic():
    # import time
    # time.sleep(12)
    if backupmanager is not None:
        return backupmanager.get_all_backup_infos()
    return []
def _load_configuration(configuration_file) -> tuple[Optional[CfgResticDash], list[str]]:
    result = load_yaml(CfgResticDash, configuration_file, True)
    to_remove: list[str] = []
    if result is not None:
        for backup in result.backups.values():
            backup.password, created = grant_password_file(backup.password)
            if created:
                to_remove.append(backup.password)
    return result, to_remove


def _setup_flask(static_dir: Optional[str]) -> StoppableFlask:

    result = StoppableFlask(__name__, configuration.settings.port, origins=configuration.settings.origins)

    api_blueprint = Blueprint('api', __name__)
    api_blueprint.add_url_rule('/restic', 'get_restic', view_get_restic)
    api_blueprint.add_url_rule('/config', 'get_frontend_config', view_get_frontend_config)
    result.register_blueprint(api_blueprint, f'{configuration.settings.context_path}/api')

    if static_dir is not None:

        static_blueprint = Blueprint('static', __name__, static_url_path='/', static_folder=static_dir)
        static_blueprint.add_url_rule('/', 'static_root', lambda: send_from_directory(static_dir, 'index.html'))
        result.register_blueprint(static_blueprint, configuration.settings.context_path)

    return result


def _shutdown(signal, frame):

    global flaskthread
    global removable_password_files
    global backupmanager

    logger.info("Shutting down...")

    if flaskthread is not None:
        try:
            flaskthread.stop()
        except Exception as ex:
            logger.error("Failed to stop flask", exc_info=ex)
        flaskthread = None

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

    # necessary to kill Flask as it doesn't expose it's internal server
    os.kill(os.getpid(), signal.SIGTERM)

    logger.info("... completed shutdown")


def _kill():

    pid = PidHandler.read_pid(configuration.settings.pidfile)
    if pid is not None:
        logger.info(f"Sending SIGINT to {pid}")
        os.kill(pid, signal.SIGINT)
    logger.info("Done")


def _resticdash(static_dir: Optional[str] = None):

    global backupmanager
    global flaskthread

    backupmanager = BackupManager(configuration)
    backupmanager.start()

    flaskthread = _setup_flask(static_dir)
    flaskthread.execute()

    _shutdown(None, None)


def main():

    global removable_password_files
    global configuration

    config_file, static_dir, kill = get_args()

    configuration, removable_password_files = _load_configuration(config_file)
    logging.basicConfig(level = configuration.settings.log_level.value[0])
    logger.setLevel(configuration.settings.log_level.value[0])

    if kill:
        _kill()
        return

    with PidHandler(configuration.settings.pidfile):
        _resticdash(static_dir)


if __name__ == '__main__':
    try:
        setproctitle(NAME)
        signal.signal(signal.SIGINT, _shutdown)
        main()
    except Exception as ex:
        logger.error(f"{NAME} failed", exc_info=ex)
        sys.exit(1)
