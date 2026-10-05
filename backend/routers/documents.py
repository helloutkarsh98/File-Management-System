from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import os
import shutil

from .. import crud, schemas
from ..database import get_db

router = APIRouter(prefix="/documents", tags=["documents"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=schemas.Document)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    return crud.create_document(db=db, document=document)

@router.get("/", response_model=List[schemas.Document])
def read_documents(skip: int = 0, limit: int = 100, search: Optional[str] = None, db: Session = Depends(get_db)):
    documents = crud.get_documents(db, skip=skip, limit=limit, search=search)
    return documents

@router.get("/{document_id}", response_model=schemas.Document)
def read_document(document_id: int, db: Session = Depends(get_db)):
    db_document = crud.get_document(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    return db_document

@router.post("/{document_id}/upload/")
def upload_document_version(document_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    db_document = crud.get_document(db, document_id=document_id)
    if db_document is None:
        raise HTTPException(status_code=404, detail="Document not found")
    
    file_path = os.path.join(UPLOAD_DIR, f"{document_id}_{file.filename}")
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    version = crud.add_document_version(db, document_id, file.filename, file_path)
    return {"message": "Version uploaded successfully", "version": version.version_number}
