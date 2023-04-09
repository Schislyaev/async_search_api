import uuid

import orjson
from pydantic import BaseModel

from .helpers import orjson_dumps


class DefaultModel(BaseModel):
    id: uuid.UUID

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
