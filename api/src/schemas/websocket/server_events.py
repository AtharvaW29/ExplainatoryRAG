from datetime import UTC, datetime
from typing import Literal
from uuid import UUID, uuid4

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    NonNegativeInt,
)


class ServerEventBase(BaseModel):
    model_config = ConfigDict(extra="forbid")

    v: Literal[1] = 1
    event_id: UUID = Field(default_factory=uuid4)
    type: str
    conversation_id: UUID | None = None
    request_id: UUID | None = None
    seq: NonNegativeInt
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class PongPayload(BaseModel):
    nonce: str | None = None


class PongEvent(ServerEventBase):
    type: Literal["pong"] = "pong"
    payload: PongPayload


class ErrorPayload(BaseModel):
    code: str
    message: str
    retryable: bool = False
    details: list[dict[str, object]] | None = None


class ErrorEvent(ServerEventBase):
    type: Literal["error"] = "error"
    payload: ErrorPayload


class ChatAcceptedPayload(BaseModel):
    user_message_id: UUID


class ChatAcceptedEvent(ServerEventBase):
    type: Literal["chat.accepted"] = "chat.accepted"
    payload: ChatAcceptedPayload


class GenerationStartedPayload(BaseModel):
    assistant_message_id: UUID
    provider: str
    model: str


class GenerationStartedEvent(ServerEventBase):
    type: Literal["generation.started"] = "generation.started"
    payload: GenerationStartedPayload


class GenerationDeltaPayload(BaseModel):
    assistant_message_id: UUID
    text: str


class GenerationDeltaEvent(ServerEventBase):
    type: Literal["generation.delta"] = "generation.delta"
    payload: GenerationDeltaPayload


class GenerationCompletedPayload(BaseModel):
    assistant_message_id: UUID
    finish_reason: Literal["stop", "length", "tool_call"]
    input_tokens: int | None = None
    output_tokens: int | None = None


class GenerationCompletedEvent(ServerEventBase):
    type: Literal["generation.completed"] = "generation.completed"
    payload: GenerationCompletedPayload


class GenerationCancelledPayload(BaseModel):
    assistant_message_id: UUID
    reason: str


class GenerationCancelledEvent(ServerEventBase):
    type: Literal["generation.cancelled"] = "generation.cancelled"
    payload: GenerationCancelledPayload
