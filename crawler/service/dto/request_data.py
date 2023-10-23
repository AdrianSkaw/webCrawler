from typing import Any

from pydantic import BaseModel


class RequestData(BaseModel):
    url: str
    list_selector: str
    config: dict
    selectors: dict
    headers: dict
