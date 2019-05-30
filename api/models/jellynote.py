from dataclasses import dataclass, field
from datetime import datetime
from enum import auto
from typing import List, NewType

from dataclasses_json import dataclass_json
from marshmallow import fields

from . import AutoName

UserId = NewType('UserId', int)


def iso_encoded_datetime():
    return field(default=datetime.now(),
                 metadata={'dataclasses_json': {
                     'encoder': datetime.isoformat,
                     'decoder': datetime.fromisoformat,
                     'mm_field': fields.DateTime(format='iso')
                 }})


class Instrument(AutoName):
    Guitar = auto()
    Piano = auto()
    Ukulele = auto()
    Violin = auto()


@dataclass_json
@dataclass(frozen=True)
class User:
    """User representation"""
    id: UserId
    name: str
    email: str
    instruments: List[Instrument] = field(default_factory=list)
    created_at: datetime = iso_encoded_datetime()
    updated_at: datetime = iso_encoded_datetime()
