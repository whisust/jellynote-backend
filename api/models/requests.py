from dataclasses import dataclass, field
from typing import List
import re
from validators import *
from dataclasses_json import dataclass_json
from marshmallow import fields

from .jellynote import Instrument

EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


@dataclass_json
@dataclass(frozen=True)
class UserCreationRequest:
    """Request to create a user"""
    name: str
    email: str
    instruments: List[Instrument] = field(metadata={'dataclasses_json': {'decoder': decode_enum_iterable(Instrument)}})

    def validate(self):
        non_empty("name")(self.name)
        match_regex("email", EMAIL_REGEX)
