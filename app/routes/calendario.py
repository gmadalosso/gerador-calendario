from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.core.enums import (
    InicioSemana,
    MAPA_INICIO_SEMANA,
    COLUNAS_DIAS_SEMANA
)

from app.services.calendario_service import gerar_calendario_anual


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def calendario(
    request: Request,
    ano: int | None = None,
    inicio_semana: InicioSemana = InicioSemana.DOMINGO
):
    ano = ano or datetime.now().year

    primeiro_dia_semana = MAPA_INICIO_SEMANA[inicio_semana.value]

    datas_calendario = gerar_calendario_anual(
        ano=ano,
        primeiro_dia_semana=primeiro_dia_semana
    )

    return templates.TemplateResponse(
        "calendario.html",
        {
            "request": request,
            "ano": ano,
            "calendario": datas_calendario,
            "dias_semana": COLUNAS_DIAS_SEMANA[inicio_semana.value],
            "inicio_semana": inicio_semana.value
        }
    )