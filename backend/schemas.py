from pydantic import BaseModel
from typing import List, Optional
import datetime

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int

    class Config:
        from_attributes = True

class DocumentVersionBase(BaseModel):
    filename: str
    file_path: str
    version_number: int

class DocumentVersionCreate(DocumentVersionBase):
    document_id: int

class DocumentVersion(DocumentVersionBase):
    id: int
    created_at: datetime.datetime

    class Config:
        from_attributes = True

class DocumentBase(BaseModel):
    title: str
    description: Optional[str] = None

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    created_at: datetime.datetime
    updated_at: datetime.datetime
    tags: List[Tag] = []
    versions: List[DocumentVersion] = []

    class Config:
        from_attributes = True
