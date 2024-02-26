import logging
import yaml

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

