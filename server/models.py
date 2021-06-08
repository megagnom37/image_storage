from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List


class Image(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    name: str
    tags: List[str] = Field(default_factory=list)
