from fastapi import FastAPI
from engine.backend.app.database.connect_db import engine, Base
from engine.backend.app.routers import tasks_router

app = FastAPI()

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app.include_router(tasks_router.router)

@app.get("/")
async def root():
    return {"message": "Welcome to SOFIA API"}


