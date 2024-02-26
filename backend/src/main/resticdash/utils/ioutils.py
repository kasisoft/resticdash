import logging
import yaml
import os

from typing import List

from resticdash.resticdashexception import ResticDashException
from resticdash.utils import validation

logger = logging.getLogger(__name__)


def load_yaml(cls, filepath: str, debug: bool = False):
    """
    Loads a YAML file and serializes its content into a json dataclass.
    """

    validation.require_file(filepath)

    logger.debug(f"Loading yaml file {filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            yaml_loaded = yaml.safe_load(content)
            result = cls.from_dict(yaml_loaded)
            if debug:
                logger.debug(f"Loaded and parse YAML:\n{result}")
            return result
    except Exception as ex:
        raise ResticDashException(f"Failed to parse '{filepath}'!", ex)


def remove_files(files: List[str]):
    """
    Removes all files within the supplied list. This function will go through all files and report errors to the log.
    """

    for file in files:
        try:
            os.remove(file)
        except Exception as ex:
            logger.error(f"Failed to delete file '{file}'.", exc_info=ex)

