from fastapi import FastAPI
from . import models
from .database import engine
from .routers import documents, tags

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Knowledge Repository API")

app.include_router(documents.router)
app.include_router(tags.router)
