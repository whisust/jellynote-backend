from configobj import ConfigObj
from typing import Optional

DEFAULT_CONF = "../resources/config.ini"


def load(filename: Optional[str] = None):
    _filename = DEFAULT_CONF if filename is None else filename
    print("Loading config file " + _filename)
    return ConfigObj(_filename)
