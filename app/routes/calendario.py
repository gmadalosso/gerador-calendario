from datetime import datetime
from pathlib import Path
import asyncio

from fastapi import APIRouter, Request, Query, HTTPException, status
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from weasyprint import HTML

from app.core.enums import (
    InicioSemana,
    MAPA_INICIO_SEMANA,
    COLUNAS_DIAS_SEMANA
)
from app.core.validators import (
    validate_ano,
    validate_uf,
    validate_orientacao
)

from app.services.calendario_service import gerar_calendario_anual
from app.services.feriados_service import (buscar_feriados_nacionais, buscar_feriados_estaduais)
from app.services.fases_lua_service import gerar_fases_lua_ano

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STATIC_DIR = BASE_DIR / "app" / "static"


async def _preparar_dados_calendario(ano: int, inicio_semana: InicioSemana, uf: str | None, mostrar_fases_lua: bool):
    primeiro_dia_semana = MAPA_INICIO_SEMANA[inicio_semana.value]

    feriados_nacionais_lista, _ = await buscar_feriados_nacionais(ano)

    feriados_nacionais = {
        f["date"]: {
            "nome": f["localName"],
            "tipo": "nacional"
        }
        for f in feriados_nacionais_lista
    }
    feriados_estaduais_raw = buscar_feriados_estaduais(uf)

    feriados_estaduais = {}

    for data_ddmm, info in feriados_estaduais_raw.items():
        dia, mes = data_ddmm.split("-")
        data_iso = f"{ano}-{mes}-{dia}"
        feriados_estaduais[data_iso] = info

    feriados_por_data = {
        **feriados_nacionais,
        **feriados_estaduais
    }

    fases_lua_por_data = gerar_fases_lua_ano(ano) if mostrar_fases_lua else {}

    eventos_por_data = {}
    lista_datas = list(feriados_por_data.keys())
    if mostrar_fases_lua:
        lista_datas = list(set(lista_datas + list(fases_lua_por_data.keys())))
    
    for data_str in lista_datas:
        evento = {}
        if data_str in feriados_por_data:
            evento["feriado"] = feriados_por_data[data_str]
        if mostrar_fases_lua and data_str in fases_lua_por_data:
            evento["fase_lua"] = fases_lua_por_data[data_str]
        if evento:
            eventos_por_data[data_str] = evento

    datas_calendario = gerar_calendario_anual(
        ano=ano,
        primeiro_dia_semana=primeiro_dia_semana,
        feriados=eventos_por_data
    )

    return {
        "ano": ano,
        "calendario": datas_calendario,
        "dias_semana": COLUNAS_DIAS_SEMANA[inicio_semana.value],
        "inicio_semana": inicio_semana.value,
        "uf": uf
    }


@router.get("/sobre", response_class=HTMLResponse)
async def sobre(request: Request):
    return templates.TemplateResponse(
        "web/sobre.html",
        {
            "request": request
        }
    )


@router.get("/", response_class=HTMLResponse)
async def form_calendario(
    request: Request,
    ano: int | None = None,
    inicio_semana: InicioSemana = InicioSemana.DOMINGO,
    uf: str | None = None,
    mostrar_fases_lua: bool = False,
    mostrar_contagem_semanas: bool = False,
    mostrar_contagem_dias_ano: bool = False,
    orientacao: str = "vertical"
):
    if ano is not None:
        try:
            ano = validate_ano(ano)
        except HTTPException:
            ano = datetime.now().year
    
    if ano is None:
        ano = datetime.now().year
    
    uf = validate_uf(uf)
    orientacao = validate_orientacao(orientacao)

    return templates.TemplateResponse(
        "web/form.html",
        {
            "request": request,
            "ano": ano,
            "inicio_semana": inicio_semana.value,
            "uf": uf,
            "mostrar_fases_lua": mostrar_fases_lua,
            "mostrar_contagem_semanas": mostrar_contagem_semanas,
            "mostrar_contagem_dias_ano": mostrar_contagem_dias_ano,
            "orientacao": orientacao
        }
    )


@router.get("/calendario/pdf")
async def gerar_pdf_calendario(
    request: Request,
    ano: int = Query(...),
    inicio_semana: InicioSemana = Query(InicioSemana.DOMINGO),
    uf: str | None = Query(None),
    mostrar_fases_lua: str | None = Query(None),
    mostrar_contagem_semanas: str | None = Query(None),
    mostrar_contagem_dias_ano: str | None = Query(None),
    orientacao: str = Query("vertical")
):
    ano = validate_ano(ano)
    uf = validate_uf(uf)
    orientacao = validate_orientacao(orientacao)

    if mostrar_fases_lua not in [None, "1", ""]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parâmetro mostrar_fases_lua inválido"
        )
    if mostrar_contagem_semanas not in [None, "1", ""]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parâmetro mostrar_contagem_semanas inválido"
        )
    if mostrar_contagem_dias_ano not in [None, "1", ""]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Parâmetro mostrar_contagem_dias_ano inválido"
        )

    mostrar_fases_lua_bool = mostrar_fases_lua == "1"
    mostrar_contagem_semanas_bool = mostrar_contagem_semanas == "1"
    mostrar_contagem_dias_ano_bool = mostrar_contagem_dias_ano == "1"

    try:
        dados = await _preparar_dados_calendario(ano, inicio_semana, uf, mostrar_fases_lua_bool)

        dados["mostrar_contagem_semanas"] = mostrar_contagem_semanas_bool
        dados["mostrar_contagem_dias_ano"] = mostrar_contagem_dias_ano_bool

        if orientacao not in ["vertical", "horizontal"]:
            orientacao = "vertical"

        template_name = f"pdf/calendario-{orientacao}.html"
        css_filename = f"calendario-{orientacao}.css"

        if ".." in template_name or "/" in template_name.replace("pdf/", ""):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Parâmetro inválido"
            )

        css_path = STATIC_DIR / "css" / css_filename
        try:
            css_path_resolved = css_path.resolve()
            static_dir_resolved = STATIC_DIR.resolve()
            if not str(css_path_resolved).startswith(str(static_dir_resolved)):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Caminho inválido"
                )
        except (OSError, ValueError):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Caminho inválido"
            )
        
        if not css_path.exists():
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Recurso não encontrado"
            )
        
        css_content = css_path.read_text(encoding="utf-8")

        html_content = templates.get_template(template_name).render(
            request=request,
            css_content=css_content,
            **dados
        )

        try:
            pdf = await asyncio.wait_for(
                asyncio.to_thread(HTML(string=html_content).write_pdf),
                timeout=30.0
            )
        except asyncio.TimeoutError:
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Timeout ao gerar PDF. Tente novamente."
            )

        if len(pdf) > 10 * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="PDF gerado excede o tamanho máximo permitido"
            )

        filename = f"calendario_{ano}.pdf"
        filename = "".join(c for c in filename if c.isalnum() or c in "._-")

        return Response(
            content=pdf,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"inline; filename={filename}",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0"
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Erro ao gerar PDF: {type(e).__name__}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao gerar PDF. Tente novamente."
        )