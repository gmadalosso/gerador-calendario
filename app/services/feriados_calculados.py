from datetime import date, timedelta
from pathlib import Path
import json


def calcular_pascoa(ano: int) -> date:
    a = ano % 19
    b = ano // 100
    c = ano % 100
    d = b // 4
    e = b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i = c // 4
    k = c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451
    n = (h + l - 7 * m + 114) // 31
    p = (h + l - 7 * m + 114) % 31
    
    mes = n
    dia = p + 1
    
    return date(ano, mes, dia)


def calcular_feriados_moveis(ano: int) -> dict[str, date]:
    pascoa = calcular_pascoa(ano)

    feriados = {
        "Carnaval": pascoa - timedelta(days=47),
        "Sexta-feira Santa": pascoa - timedelta(days=2),
        "Páscoa": pascoa,
        "Corpus Christi": pascoa + timedelta(days=60),
    }
    
    return feriados


def carregar_feriados_fixos() -> dict[str, str]:
    BASE_DIR = Path(__file__).resolve().parent.parent
    FERIADOS_NACIONAIS_PATH = BASE_DIR / "data" / "feriados_nacionais.json"
    
    if not FERIADOS_NACIONAIS_PATH.exists():
        return {}
    
    with open(FERIADOS_NACIONAIS_PATH, encoding="utf-8") as f:
        dados = json.load(f)
    
    feriados = {}
    for item in dados:
        feriados[item["data"]] = item["nome"]
    
    return feriados


def calcular_feriados_nacionais(ano: int) -> dict[str, dict]:
    feriados_fixos_raw = carregar_feriados_fixos()

    feriados_fixos = {}
    for data_ddmm, nome in feriados_fixos_raw.items():
        dia, mes = data_ddmm.split("-")
        data_iso = f"{ano}-{mes}-{dia}"
        feriados_fixos[data_iso] = {
            "nome": nome,
            "tipo": "nacional"
        }

    feriados_moveis = calcular_feriados_moveis(ano)

    feriados_moveis_dict = {}
    for nome, data in feriados_moveis.items():
        data_str = data.isoformat()
        feriados_moveis_dict[data_str] = {
            "nome": nome,
            "tipo": "nacional"
        }

    todos_feriados = {**feriados_fixos, **feriados_moveis_dict}
    
    return todos_feriados


def buscar_feriados_nacionais_calculados(ano: int) -> tuple[list[dict], bool]:
    feriados_dict = calcular_feriados_nacionais(ano)

    feriados_lista = []
    for data_str, info in feriados_dict.items():
        feriados_lista.append({
            "date": data_str,
            "localName": info["nome"],
            "global": True
        })
    
    return feriados_lista, True

