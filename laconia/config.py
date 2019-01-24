import pathlib
from pathlib import Path

from marshmallow import UnmarshalResult
from yaml import safe_load

from laconia.schemas import ConfigSchema

BASE_DIR = pathlib.Path(__file__).parent.parent
DEFAULT_CONFIG_PATH = BASE_DIR / "laconia.yml"


def load_config(config_path: Path) -> dict:
    """
    Load config from a given path.

    :param config_path:
    :return: config dict
    """
    with config_path.open() as config_file:
        config: dict = safe_load(config_file)

    loaded: UnmarshalResult = ConfigSchema(strict=True).load(config)

    return loaded.data


config = load_config(DEFAULT_CONFIG_PATH)
