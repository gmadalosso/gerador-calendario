import calendar
from typing import List, Dict
from app.core.enums import MESES_PORTUGUES

def gerar_calendario_anual(ano: int, primeiro_dia_semana: int = calendar.SUNDAY) -> List[Dict]:

    cal = calendar.Calendar(primeiro_dia_semana)

    calendario_anual = []

    for mes in range(1, 13):  #de 1 a 12
        datas_do_mes = {
            "mes": mes,
            "nome_mes": MESES_PORTUGUES[mes],
            "semanas": []
        }


        semanas = cal.monthdayscalendar(ano, mes)

        for semana in semanas:
            dias_da_semana = []

            for dia in semana:
                dias_da_semana.append(
                    {
                        "dia": dia if dia != 0 else None
                    }
                )

            datas_do_mes["semanas"].append(dias_da_semana)

        calendario_anual.append(datas_do_mes)

    return calendario_anual
