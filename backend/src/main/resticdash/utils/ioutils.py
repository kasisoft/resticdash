import json
import logging

from resticdash.resticdashexception import ResticDashException
from resticdash.utils import validation

logger = logging.getLogger(__name__)


def load_json(cls, filepath: str, debug: bool = False):
    """
    Loads a JSON file and serializes its content into a json dataclass.
    """

    validation.require_file(filepath)

    logger.debug(f"Loading json file {filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            json_loaded = json.loads(content)
            result = cls.from_dict(json_loaded)
            if debug:
                logger.debug(f"Loaded and parse YAML:\n{result}")
            return result
    except Exception as ex:
        raise ResticDashException(f"Failed to parse '{filepath}'!", ex)

