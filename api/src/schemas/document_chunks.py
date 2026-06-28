from typing import Any, Dict, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DocumentChunkCreate(BaseModel):
    source_id: UUID
    chunk_text: Optional[str] = None
    metadata_json: Optional[Dict[str, Any]] = Field(
        default=None, alias="metadata"
    )

    model_config = ConfigDict(populate_by_name=True)


class DocumentChunkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: UUID
    source_id: UUID
    chunk_text: Optional[str]
    metadata_json: Optional[Dict[str, Any]] = Field(..., alias="metadata")
