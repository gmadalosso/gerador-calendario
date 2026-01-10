from fastapi import HTTPException, status

ANO_MINIMO = 1900
ANO_MAXIMO = 2200
NUM_DIGITOS_UF_MAX = 2
ORIENTACOES_VALIDAS = ["vertical", "horizontal"]
UFS_VALIDAS = {
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA",
    "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN",
    "RO", "RR", "RS", "SC", "SE", "SP", "TO"
}


def validate_ano(ano: int) -> int:
    if not isinstance(ano, int):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ano deve ser um número inteiro"
        )
    
    if ano < ANO_MINIMO or ano > ANO_MAXIMO:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ano deve estar entre {ANO_MINIMO} e {ANO_MAXIMO}"
        )
    
    return ano


def validate_uf(uf: str | None) -> str | None:
    if uf is None:
        return None
    
    if not isinstance(uf, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="UF deve ser uma string"
        )
    
    uf = uf.strip().upper()
    
    if len(uf) > NUM_DIGITOS_UF_MAX:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="UF inválida"
        )
    
    if uf and uf not in UFS_VALIDAS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="UF inválida"
        )
    
    return uf if uf else None


def validate_orientacao(orientacao: str) -> str:
    if not isinstance(orientacao, str):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Orientação deve ser uma string"
        )
    
    orientacao = orientacao.strip().lower()
    
    if orientacao not in ORIENTACOES_VALIDAS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Orientação deve ser uma de: {', '.join(ORIENTACOES_VALIDAS)}"
        )
    
    return orientacao

