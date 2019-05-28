from configobj import ConfigObj

DEFAULT_CONF = "../resources/config.ini"


def load(filename):
    _filename = DEFAULT_CONF if filename is None else filename
    print("Loading config file " + _filename)
    return ConfigObj(_filename)
