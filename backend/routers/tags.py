from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/documents", tags=["tags"])

@router.post("/{document_id}/tags/", response_model=schemas.Document)
def add_tag(document_id: int, tag_name: str, db: Session = Depends(get_db)):
    db_document = crud.add_tag_to_document(db, document_id, tag_name)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document

@router.delete("/{document_id}/tags/{tag_name}", response_model=schemas.Document)
def remove_tag(document_id: int, tag_name: str, db: Session = Depends(get_db)):
    db_document = crud.remove_tag_from_document(db, document_id, tag_name)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document
