from fastapi import FastAPI
from fastapi.templating import Jinja2Templates

from app.routes.calendario import router as calendario_router

app = FastAPI(title="Gerador de Calendário")

templates = Jinja2Templates(directory="app/templates")

app.include_router(calendario_router)
