from dataclasses import dataclass, field
from dataclasses_json import dataclass_json

@dataclass_json
@dataclass(frozen=True)
class BaseError:
    message: str