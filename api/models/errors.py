import traceback
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BaseError(Exception):
    message: str


@dataclass_json
@dataclass
class NotFoundError(BaseError):
    message: str


def map_error(e: Exception):
    import sys
    from marshmallow import ValidationError
    if isinstance(e, ValueError):
        response, code = (BaseError("Invalid field : " + e.args[0]), 400)
    elif isinstance(e, KeyError):
        response, code = (BaseError("Missing field : " + e.args[0]), 400)
    elif isinstance(e, ValidationError):
        response, code = (BaseError(e.args), 400)
    else:
        traceback.print_exc(15, sys.stderr)
        response, code = (BaseError("Unexpected exception : " + repr(e)), 500)
    return response, code
