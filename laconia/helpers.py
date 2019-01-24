from functools import partial
from secrets import choice
from string import ascii_letters, digits
from urllib.parse import urljoin

from laconia.config import config

ALPHABET = ascii_letters + digits

enable_https = config["enable_https"]
key_length = config["key_length"]
host = config["host"]
url_schema = "https://" if enable_https else "http://"


def _generate_key(alphabet: str, length: int) -> str:
    """
    Generate a random string key of a given length from an alphabet.

    :param alphabet: string sequence
    :param length: required key length
    :return: generated key
    """
    return "".join(choice(alphabet) for _ in range(length))


generate_key = partial(_generate_key, ALPHABET, key_length)


def _construct_url(host: str, key: str) -> str:
    return urljoin(host, key)


construct_url = partial(_construct_url, url_schema + host)
