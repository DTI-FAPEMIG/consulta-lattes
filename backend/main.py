from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from slowapi.util import get_remote_address

from core.config import settings
from api.v1 import lattes

# Instância do Limiter para evitar ataques ou bugs de lopping que suguem recursos
limiter = Limiter(key_func=get_remote_address, default_limits=["50/minute"]) if settings.RATE_LIMIT_ENABLED else None

app = FastAPI(title=settings.PROJECT_NAME)

print("ALLOWED_ORIGINS RAW:", settings.ALLOWED_ORIGINS)
print("ALLOWED_ORIGINS LIST:", settings.allowed_origins_list)

if limiter:
    app.state.limiter = limiter
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Segurança no CORS - Restrito ao domínio da empresa
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Adicionamos as rotas do lattes no prefixo padronizado
app.include_router(lattes.router, prefix="/api/v1", tags=["lattes"])

@app.get("/health")
async def health_check():
    """ Rota pública super leve para balanciadores de carga testarem saude do server """
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    # Em produção, recomenda-se rodar via terminal: uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False)
