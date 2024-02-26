import logging
import signal
import sys

from setproctitle import setproctitle

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
    pass


if __name__ == '__main__':
    try:
        setproctitle(NAME)
        signal.signal(signal.SIGINT, _shutdown)
        main()
    except Exception as ex:
        logger.error(f"{NAME} failed", exc_info=ex)
        sys.exit(1)
