from typing import Annotated, Literal
from uuid import UUID

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    TypeAdapter,
)


class ClientEventBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    v: Literal[1] = 1
    type: str
    request_id: UUID


class PingPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    nonce: str | None = Field(default=None, max_length=100)


class PingEvent(ClientEventBase):
    type: Literal["ping"] = "ping"
    payload: PingPayload


class ChatSendPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    conversation_id: UUID | None = None
    content: str = Field(min_length=1, max_length=32_000)


class ChatSendEvent(ClientEventBase):
    type: Literal["chat.send"] = "chat.send"
    payload: ChatSendPayload


class GenerationCancelPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    generation_request_id: UUID


class GenerationCancelEvent(ClientEventBase):
    type: Literal["generation.cancel"] = "generation.cancel"
    payload: GenerationCancelPayload


ClientEvent = Annotated[
    PingEvent | ChatSendEvent | GenerationCancelEvent,
    Field(discriminator="type"),
]

client_event_adapter: TypeAdapter[ClientEvent] = TypeAdapter(ClientEvent)
