from dataclasses import dataclass, field
from datetime import datetime
from enum import auto
from typing import List, NewType

from dataclasses_json import dataclass_json
from marshmallow import fields

from . import AutoName

UserId = NewType('UserId', int)

iso_encoded_datetime = field(
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
    mail: str
    created_at: datetime = iso_encoded_datetime
    instruments: List[Instrument] = field(default_factory=list)
