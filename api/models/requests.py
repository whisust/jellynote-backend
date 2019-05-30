from dataclasses import dataclass, field
from typing import List
import re
from validators import *
from serde import *
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
        non_empty("instruments")(self.instruments)
        match_regex("email", EMAIL_REGEX)(self.email)


@dataclass_json
@dataclass(frozen=True)
class UserUpdateRequest:
    """Request to update a user"""
    name: Optional[str] = None
    email: Optional[str] = None
    instruments: Optional[List[Instrument]] = field(default=None, metadata={'dataclasses_json': {
        'decoder': decode_enum_iterable(Instrument)}}
    )

    def validate(self):
        non_all_empty(["name", "email", "instruments"])
        if self.name is not None:
            non_empty("name")(self.name)

        if self.instruments is not None:
            non_empty("instruments")(self.instruments)

        if self.email is not None:
            match_regex("email", EMAIL_REGEX)(self.email)


UserCreationRequestSchema = UserCreationRequest.schema()
UserUpdateRequestSchema = UserUpdateRequest.schema()
