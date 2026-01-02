from fastapi import FastAPI
from app.routes.calendario import router as calendario_router

app = FastAPI(title="Gerador de Calendário")

app.include_router(calendario_router)