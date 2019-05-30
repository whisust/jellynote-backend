from dataclasses import dataclass
from typing import List
import re

from dataclasses_json import dataclass_json

from .jellynote import Instrument

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


@dataclass_json
@dataclass(frozen=True)
class UserCreationRequest:
    name: str
    email: str
    instruments: List[Instrument]




