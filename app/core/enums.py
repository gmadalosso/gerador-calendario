import calendar
from enum import Enum

class InicioSemana(Enum):
    SEGUNDA = "segunda"
    TERCA = "terca"
    QUARTA = "quarta"
    QUINTA = "quinta"
    SEXTA = "sexta"
    SABADO = "sabado"
    DOMINGO = "domingo"

MAPA_INICIO_SEMANA = {
    InicioSemana.SEGUNDA.value: calendar.MONDAY,
    InicioSemana.TERCA.value: calendar.TUESDAY,
    InicioSemana.QUARTA.value: calendar.WEDNESDAY,
    InicioSemana.QUINTA.value: calendar.THURSDAY,
    InicioSemana.SEXTA.value: calendar.FRIDAY,
    InicioSemana.SABADO.value: calendar.SATURDAY,
    InicioSemana.DOMINGO.value: calendar.SUNDAY,
}

COLUNAS_DIAS_SEMANA = {
    InicioSemana.SEGUNDA.value: ["Seg", "Ter", "Qua", "Qui", "Sex", "Sáb", "Dom"],
    InicioSemana.TERCA.value: ["Ter", "Qua", "Qui", "Sex", "Sáb", "Dom", "Seg"],
    InicioSemana.QUARTA.value: ["Qua", "Qui", "Sex", "Sáb", "Dom", "Seg", "Ter"],
    InicioSemana.QUINTA.value: ["Qui", "Sex", "Sáb", "Dom", "Seg", "Ter", "Qua"],
    InicioSemana.SEXTA.value: ["Sex", "Sáb", "Dom", "Seg", "Ter", "Qua", "Qui"],
    InicioSemana.SABADO.value: ["Sáb", "Dom", "Seg", "Ter", "Qua", "Qui", "Sex"],
    InicioSemana.DOMINGO.value: ["Dom", "Seg", "Ter", "Qua", "Qui", "Sex", "Sáb"],
}

class Mes(Enum):
    JANEIRO = 1
    FEVEREIRO = 2
    MARCO = 3
    ABRIL = 4
    MAIO = 5
    JUNHO = 6
    JULHO = 7
    AGOSTO = 8
    SETEMBRO = 9
    OUTUBRO = 10
    NOVEMBRO = 11
    DEZEMBRO = 12


MESES_PORTUGUES = {
    Mes.JANEIRO.value: "Janeiro",
    Mes.FEVEREIRO.value: "Fevereiro",
    Mes.MARCO.value: "Março",
    Mes.ABRIL.value: "Abril",
    Mes.MAIO.value: "Maio",
    Mes.JUNHO.value: "Junho",
    Mes.JULHO.value: "Julho",
    Mes.AGOSTO.value: "Agosto",
    Mes.SETEMBRO.value: "Setembro",
    Mes.OUTUBRO.value: "Outubro",
    Mes.NOVEMBRO.value: "Novembro",
    Mes.DEZEMBRO.value: "Dezembro",
}
