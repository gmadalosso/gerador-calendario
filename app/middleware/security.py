import os
from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import time
from collections import defaultdict

_armazenamento_rate_limit: dict[str, tuple[float, int]] = defaultdict(lambda: (0.0, 0))
_INTERVALO_LIMPEZA = 300
_ultima_limpeza = time.time()


def _limpar_entradas_antigas():
    global _ultima_limpeza, _armazenamento_rate_limit
    tempo_atual = time.time()

    if tempo_atual - _ultima_limpeza > _INTERVALO_LIMPEZA:
        tempo_corte = tempo_atual - 60
        chaves_remover = [
            chave for chave, (data_hora, _) in _armazenamento_rate_limit.items()
            if data_hora < tempo_corte
        ]
        for chave in chaves_remover:
            del _armazenamento_rate_limit[chave]
        _ultima_limpeza = tempo_atual


def verificar_rate_limit(ip_cliente: str, limit: int = 30, window: int = 60) -> bool:
    _limpar_entradas_antigas()

    tempo_atual = time.time()
    ultima_requisicao_tempo, contador = _armazenamento_rate_limit[ip_cliente]

    if tempo_atual - ultima_requisicao_tempo > window:
        _armazenamento_rate_limit[ip_cliente] = (tempo_atual, 1)
        return True

    if contador < limit:
        _armazenamento_rate_limit[ip_cliente] = (ultima_requisicao_tempo, contador + 1)
        return True

    return False


def obter_ip_cliente(request: Request) -> str:
    encaminhado_por = request.headers.get("x-forwarded-for")
    if encaminhado_por:
        return encaminhado_por.split(",")[0].strip()

    ip_real = request.headers.get("x-real-ip")
    if ip_real:
        return ip_real

    if request.client:
        return request.client.host

    return "unknown"


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        resposta = await call_next(request)

        ambiente = os.getenv("ENVIRONMENT", "production")

        resposta.headers["X-Content-Type-Options"] = "nosniff"
        resposta.headers["X-Frame-Options"] = "SAMEORIGIN"
        resposta.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        resposta.headers["X-XSS-Protection"] = "1; mode=block"

        csp = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; "
            "font-src 'self' https://cdn.jsdelivr.net; "
            "img-src 'self' data:; "
            "frame-ancestors 'self';"
        )
        resposta.headers["Content-Security-Policy"] = csp
        
        return resposta


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp, limit: int = 30, window: int = 60):
        super().__init__(app)
        self.limit = limit
        self.window = window

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/calendario/"):
            ip_cliente = obter_ip_cliente(request)

            limite_pdf = 10 if "/pdf" in request.url.path else self.limit
            
            if not verificar_rate_limit(ip_cliente, limit=limite_pdf, window=self.window):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Muitas requisições. Por favor, tente novamente em alguns instantes."
                )
        
        resposta = await call_next(request)
        return resposta

