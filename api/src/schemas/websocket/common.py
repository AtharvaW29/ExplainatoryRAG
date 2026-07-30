from datetime import UTC, datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, NonNegativeInt


class ServerEventBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    v: Literal[1] = 1
    event_id: UUID = Field(default_factory=uuid4)
    type: str
    conversation_id: UUID | None = None
    request_id: UUID | None = None
    seq: NonNegativeInt
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
