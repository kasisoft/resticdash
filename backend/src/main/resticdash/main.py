import logging
import signal
import sys
import os

from typing import Optional
from setproctitle import setproctitle

from resticdash.utils.ioutils import load_yaml
from resticdash.config import CfgResticDash
from resticdash.getargs import get_args
from resticdash.utils.pidutils import PidHandler

NAME = "resticdash"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(module)s - %(message)s',
    datefmt="%H:%M:%S"
)

logger = logging.getLogger(NAME)

configuration: Optional[CfgResticDash] = None


def _shutdown(signal, frame):
    pass


def _kill():

    pid = PidHandler.read_pid(configuration.settings.pidfile)
    if pid is not None:
        logger.info(f"Sending SIGINT to {pid}")
        os.kill(pid, signal.SIGINT)
    logger.info("Done")


def main():

    global configuration
    global logger

    config_file, kill = get_args()
    logger.info(f"Config file: {config_file}")

    configuration = load_yaml(CfgResticDash, config_file)
    logging.basicConfig(level = configuration.settings.log_level.value[0])
    logger.setLevel(configuration.settings.log_level.value[0])

    if kill:
        _kill()
        return

    with PidHandler(configuration.settings.pidfile):
        pass


if __name__ == '__main__':
    try:
        setproctitle(NAME)
        signal.signal(signal.SIGINT, _shutdown)
        main()
    except Exception as ex:
        logger.error(f"{NAME} failed", exc_info=ex)
        sys.exit(1)
