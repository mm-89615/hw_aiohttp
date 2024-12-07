from typing import Optional

from aiohttp.web import HTTPBadRequest
from pydantic import BaseModel, ValidationError

from utils.generate_error import generate_error


class CreateAdvertisementSchema(BaseModel):
    title: str
    description: Optional[str]
    owner: str


class UpdateAdvertisementSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    owner: Optional[str] = None


def validate_json(json_data, schema_cls):
    try:
        schema_obj = schema_cls(**json_data)
        json_data_validated = schema_obj.dict(exclude_unset=True)
        return json_data_validated
    except ValidationError as err:
        errors = err.errors()
        for error in errors:
            error.pop("ctx", None)
        raise generate_error(HTTPBadRequest, errors)
