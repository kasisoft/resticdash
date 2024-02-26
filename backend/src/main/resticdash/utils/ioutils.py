import tempfile
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


def create_temp_file(content: str) -> str:
    """
    Creates a temporary file with the supplied content and returns it's path.
    """

    try:

        with tempfile.NamedTemporaryFile(mode='w+', delete=False, encoding='utf-8') as temp_file:
            result = temp_file.name
            temp_file.write(content)

        # user readable only
        os.chmod(result, 0o400)
        return result

    except Exception as ex:
        raise ResticDashException(f"Failed to create a temporary file !", ex)


def remove_files(files: List[str]):
    """
    Removes all files within the supplied list. This function will go through all files and report errors to the log.
    """

    for file in files:
        try:
            os.remove(file)
        except Exception as ex:
            logger.error(f"Failed to delete file '{file}'.", exc_info=ex)


def grant_password_file(password: str) -> (str, bool):
    """
    Makes sure to return a file containing the supplied password. If the supplied password value already refers to a file
    with a password it will be returned as is. Otherwise a temporary file with the supplied password will be created and
    returned. This function returns a tupel in which the second value is a boolean indicating whether a file had to be
    created or not.
    """

    if os.path.isfile(password):
        # the user directly provided a password file so return it
        return password, False

    return create_temp_file(password), True
