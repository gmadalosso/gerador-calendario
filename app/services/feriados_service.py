import json
from pathlib import Path

from app.services.feriados_calculados import buscar_feriados_nacionais_calculados

BASE_DIR = Path(__file__).resolve().parent.parent
FERIADOS_ESTADUAIS_PATH = BASE_DIR / "data" / "feriados_estaduais.json"


async def buscar_feriados_nacionais(ano: int) -> tuple[list[dict], bool]:
    return buscar_feriados_nacionais_calculados(ano)

def buscar_feriados_estaduais(uf: str | None) -> dict[str, dict]:
    if not uf:
        return {}

    uf = uf.upper()

    if not FERIADOS_ESTADUAIS_PATH.exists():
        return {}

    with open(FERIADOS_ESTADUAIS_PATH, encoding="utf-8") as f:
        dados = json.load(f)

    feriados = {}

    for item in dados.get(uf, []):
        feriados[item["data"]] = {
            "nome": item["nome"],
            "tipo": "estadual",
            "uf": uf
        }

    return feriados