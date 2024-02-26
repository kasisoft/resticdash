import argparse
import logging
import os

from typing import Optional
from resticdash.utils.validation import require_file, require_directory

logger = logging.getLogger(__name__)


def _locate_static_dir(folder: Optional[str]) -> Optional[str]:
    if folder is None:
        logger.warning("No static directory supplied thus not serving any static files")
        return None
    result = os.path.normpath(os.path.abspath(folder))
    logger.debug(f"Using static directory '{result}' !")
    require_directory(result)
    return result


def _locate_configuration_file(configfile: str) -> str:
    result = os.path.normpath(os.path.abspath(configfile))
    logger.debug(f"Using configuration file '{result}'!")
    require_file(result)
    return result


def get_args() -> tuple[str, Optional[str], bool]:

    parser = argparse.ArgumentParser(
        prog='resticdash',
        description='Provides API endpoints to query restic snapshot infos for display',
        epilog='-- Daniel Kasmeroglu (daniel.kasmeroglu@kasisoft.com) (change to github!)'
    )

    parser.add_argument('-s', '--static', help='Location of the frontend code', required=False)
    parser.add_argument('-c', '--config', help='Location of the configuration file', default='resticdash.yaml')
    parser.add_argument('-k', '--kill', help='Kill a potential existing instance', action='store_true')

    args = parser.parse_args()

    static_dir = _locate_static_dir(args.static)
    config_file = _locate_configuration_file(args.config)

    return config_file, static_dir, args.kill

