import os
from dataclasses import dataclass

to_int = lambda x: int(x)


def _envOr(varname, default_value, mapper=lambda x: x):
    env = os.environ.get(varname)
    return default_value if env is None else mapper(env)

# Inspired by the scala pureconfig way, define all your conf in immutable data classes.

@dataclass(frozen=True)
class ServerConfig:
    port: int = _envOr('SERVER_PORT', 5050, to_int)
    host: str = _envOr('SERVER_HOST', '127.0.0.1')


@dataclass(frozen=True)
class DBConfig:
    port: int = _envOr('DB_PORT', 5432, to_int)
    host: str = _envOr('DB_HOST', 'localhost')
    user: str = _envOr('DB_USER', 'jelly')
    password: str = _envOr('DB_PASSWORD', 'j3llynote')
    database: str = _envOr('DB_NAME', 'jellynote')


@dataclass(frozen=True)
class Config:
    server: ServerConfig = ServerConfig()
    db: DBConfig = DBConfig()
    env: str = _envOr('ENV', 'dev')


conf = Config()