import datetime
import calendar

from app.core.enums import MESES_PORTUGUES


def gerar_calendario_anual(
    ano: int,
    primeiro_dia_semana: int = calendar.SUNDAY,
    feriados: dict[str, dict] | None = None
) -> list[dict[str, object]]:
    cal = calendar.Calendar(primeiro_dia_semana)

    calendario_anual: list[dict[str, object]] = []

    primeiro_janeiro = datetime.date(ano, 1, 1)
    offset_domingo = (primeiro_janeiro.weekday() + 1) % 7
    domingo_semana_1 = primeiro_janeiro - datetime.timedelta(days=offset_domingo)

    for mes in range(1, 13):
        datas_do_mes = {
            "mes": mes,
            "nome_mes": MESES_PORTUGUES[mes],
            "semanas": []
        }

        semanas = cal.monthdayscalendar(ano, mes)

        indice_coluna_domingo = (6 - primeiro_dia_semana) % 7
        if mes == 1:
            mes_anterior = 12
            ano_anterior = ano - 1
        else:
            mes_anterior = mes - 1
            ano_anterior = ano

        if mes == 12:
            mes_seguinte = 1
            ano_seguinte = ano + 1
        else:
            mes_seguinte = mes + 1
            ano_seguinte = ano

        for semana in semanas:
            dias_da_semana = []

            for indice_coluna, dia in enumerate(semana):
                if indice_coluna == indice_coluna_domingo:
                    if dia != 0:
                        domingo = datetime.date(ano, mes, dia)
                    else:
                        if semana == semanas[0]:
                            ultimo_dia_mes_anterior = calendar.monthrange(
                                ano_anterior, mes_anterior
                            )[1]
                            domingo = datetime.date(
                                ano_anterior,
                                mes_anterior,
                                ultimo_dia_mes_anterior
                            )
                        else:
                            domingo = datetime.date(
                                ano_seguinte,
                                mes_seguinte,
                                1
                            )
                    break

            delta_dias = (domingo - domingo_semana_1).days
            numero_semana = (delta_dias // 7) + 1

            for indice_coluna, dia in enumerate(semana):
                dia_mes_adjacente = None
                mes_adjacente = False

                if dia:
                    data = datetime.date(ano, mes, dia)
                    data_str = data.isoformat()
                    marcador_domingo = data.weekday() == 6
                    dia_do_ano = data.timetuple().tm_yday
                else:
                    data_str = None
                    marcador_domingo = indice_coluna == indice_coluna_domingo
                    dia_do_ano = None

                    primeira_semana = semana == semanas[0]
                    ultima_semana = semana == semanas[-1]

                    if primeira_semana:
                        primeiro_dia_index = next(
                            (i for i, d in enumerate(semana) if d != 0),
                            None
                        )
                        if primeiro_dia_index is not None and indice_coluna < primeiro_dia_index:
                            dias_no_mes_anterior = calendar.monthrange(
                                ano_anterior, mes_anterior
                            )[1]
                            posicao_relativa = primeiro_dia_index - indice_coluna - 1
                            dia_mes_adjacente = dias_no_mes_anterior - posicao_relativa
                            mes_adjacente = True

                    if ultima_semana:
                        ultimo_dia_index = next(
                            (i for i in range(len(semana) - 1, -1, -1) if semana[i] != 0),
                            None
                        )
                        if ultimo_dia_index is not None and indice_coluna > ultimo_dia_index:
                            celulas_vazias_apos = indice_coluna - ultimo_dia_index
                            dia_mes_adjacente = celulas_vazias_apos
                            mes_adjacente = True

                evento = feriados.get(data_str) if feriados and data_str else None

                dias_da_semana.append({
                    "dia": dia if dia != 0 else None,
                    "dia_do_ano": dia_do_ano,
                    "dia_mes_adjacente": dia_mes_adjacente,
                    "mes_adjacente": mes_adjacente,
                    "feriado": evento.get("feriado") if evento else None,
                    "fase_lua": evento.get("fase_lua") if evento else None,
                    "marcador_domingo": marcador_domingo
                })

            datas_do_mes["semanas"].append({
                "numero_semana": numero_semana,
                "dias": dias_da_semana
            })

        calendario_anual.append(datas_do_mes)

    return calendario_anual
