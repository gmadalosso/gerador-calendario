from datetime import datetime
import ephem


def gerar_fases_lua_ano(ano: int) -> dict[str, str]:
    fases = {}

    data_inicio = datetime(ano, 1, 1)
    data_fim = datetime(ano, 12, 31, 23, 59, 59)

    data_atual_ephem = ephem.Date(data_inicio)
    data_fim_ephem = ephem.Date(data_fim)

    lua_nova = ephem.previous_new_moon(data_atual_ephem)

    while lua_nova < data_fim_ephem:
        data_ephem_tupla = ephem.Date(lua_nova).tuple()
        data_dt = datetime(int(data_ephem_tupla[0]), int(data_ephem_tupla[1]), int(data_ephem_tupla[2]))

        if data_dt.year == ano:
            data_str = data_dt.strftime("%Y-%m-%d")
            fases[data_str] = "Lua Nova"

        quarto_crescente = ephem.next_first_quarter_moon(lua_nova)
        data_qc_tupla = ephem.Date(quarto_crescente).tuple()
        data_qc_dt = datetime(int(data_qc_tupla[0]), int(data_qc_tupla[1]), int(data_qc_tupla[2]))
        if data_qc_dt.year == ano:
            data_str = data_qc_dt.strftime("%Y-%m-%d")
            fases[data_str] = "Quarto Crescente"

        lua_cheia = ephem.next_full_moon(lua_nova)
        data_lc_tupla = ephem.Date(lua_cheia).tuple()
        data_lc_dt = datetime(int(data_lc_tupla[0]), int(data_lc_tupla[1]), int(data_lc_tupla[2]))
        if data_lc_dt.year == ano:
            data_str = data_lc_dt.strftime("%Y-%m-%d")
            fases[data_str] = "Lua Cheia"

        quarto_minguante = ephem.next_last_quarter_moon(lua_nova)
        data_qm_tupla = ephem.Date(quarto_minguante).tuple()
        data_qm_dt = datetime(int(data_qm_tupla[0]), int(data_qm_tupla[1]), int(data_qm_tupla[2]))
        if data_qm_dt.year == ano:
            data_str = data_qm_dt.strftime("%Y-%m-%d")
            fases[data_str] = "Quarto Minguante"

        lua_nova = ephem.next_new_moon(lua_nova)

    return fases