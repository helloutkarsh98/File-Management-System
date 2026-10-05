from sqlalchemy.orm import Session
from sqlalchemy import or_
from . import models, schemas
import os

def get_document(db: Session, document_id: int):
    return db.query(models.Document).filter(models.Document.id == document_id).first()

def get_documents(db: Session, skip: int = 0, limit: int = 100, search: str = None):
    query = db.query(models.Document)
    if search:
        query = query.filter(
            or_(
                models.Document.title.ilike(f"%{search}%"),
                models.Document.description.ilike(f"%{search}%")
            )
        )
    return query.offset(skip).limit(limit).all()

def create_document(db: Session, document: schemas.DocumentCreate):
    db_document = models.Document(**document.model_dump())
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def add_document_version(db: Session, document_id: int, filename: str, file_path: str):
    # Find latest version
    latest_version = db.query(models.DocumentVersion)\
        .filter(models.DocumentVersion.document_id == document_id)\
        .order_by(models.DocumentVersion.version_number.desc()).first()
    
    version_number = 1
    if latest_version:
        version_number = latest_version.version_number + 1

    db_version = models.DocumentVersion(
        document_id=document_id,
        filename=filename,
        file_path=file_path,
        version_number=version_number
    )
    db.add(db_version)
    
    # Update document updated_at
    document = get_document(db, document_id)
    if document:
        import datetime
        document.updated_at = datetime.datetime.utcnow()
    
    db.commit()
    db.refresh(db_version)
    return db_version

def get_tag_by_name(db: Session, name: str):
    return db.query(models.Tag).filter(models.Tag.name == name).first()

def add_tag_to_document(db: Session, document_id: int, tag_name: str):
    document = get_document(db, document_id)
    if not document:
        return None
    
    tag = get_tag_by_name(db, tag_name)
    if not tag:
        tag = models.Tag(name=tag_name)
        db.add(tag)
        db.commit()
        db.refresh(tag)
    
    if tag not in document.tags:
        document.tags.append(tag)
        db.commit()
        db.refresh(document)
    
    return document

def remove_tag_from_document(db: Session, document_id: int, tag_name: str):
    document = get_document(db, document_id)
    tag = get_tag_by_name(db, tag_name)
    
    if document and tag and tag in document.tags:
        document.tags.remove(tag)
        db.commit()
        db.refresh(document)
        
    return document
