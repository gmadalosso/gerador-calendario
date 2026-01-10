import os
from pathlib import Path
from fastapi import FastAPI, Request, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from app.routes.calendario import router as calendario_router
from app.middleware.security import SecurityHeadersMiddleware, RateLimitMiddleware

ENVIRONMENT = os.getenv("ENVIRONMENT", "production")

import sys
if ENVIRONMENT == "development":
    sys.stderr.write("⚠️  AMBIENTE DE DESENVOLVIMENTO\n")
    sys.stderr.flush()

app = FastAPI()

app.add_middleware(SecurityHeadersMiddleware)
app.add_middleware(RateLimitMiddleware, limit=30, window=60)

origens_permitidas = os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else []
if not origens_permitidas:
    origens_permitidas = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origens_permitidas,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"
if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

app.include_router(calendario_router)


@app.exception_handler(RequestValidationError)
async def tratar_excecao_validacao(request: Request, excecao: RequestValidationError):
    if ENVIRONMENT == "development":
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": excecao.errors()}
        )
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Parâmetros inválidos"}
    )


@app.exception_handler(Exception)
async def tratar_excecao_geral(request: Request, excecao: Exception):
    if ENVIRONMENT == "development":
        import traceback
        print(f"Erro: {excecao}\n{traceback.format_exc()}")
    else:
        print(f"Erro: {type(excecao).__name__}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno do servidor"}
    )
