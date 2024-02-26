import argparse
import logging
import os

from resticdash.utils.validation import require_file

logger = logging.getLogger(__name__)


def _locate_configuration_file(configfile: str) -> str:
    result = os.path.normpath(os.path.abspath(configfile))
    logger.debug(f"Using configuration file '{result}'!")
    require_file(result)
    return result


def get_args() -> tuple[str, bool]:

    parser = argparse.ArgumentParser(
        prog='resticdash',
        description='Provides API endpoints to query restic snapshot infos for display',
        epilog='-- Daniel Kasmeroglu (daniel.kasmeroglu@kasisoft.com) (change to github!)'
    )

    parser.add_argument('-c', '--config', help='Location of the configuration file', default='resticdash.yaml')
    parser.add_argument('-k', '--kill', help='Kill a potential existing instance', action='store_true')

    args = parser.parse_args()

    config_file = _locate_configuration_file(args.config)

    return config_file, args.kill
