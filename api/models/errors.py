from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass_json
class BaseError(Exception):
    message: str
