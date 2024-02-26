import logging
import signal
import sys

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


def _shutdown(signal, frame):
    pass


def main():

    config_file = get_args()
    logger.info(f"Config file: {config_file}")

    configuration = load_yaml(CfgResticDash, config_file)
    logger.info(f"{configuration}")

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
