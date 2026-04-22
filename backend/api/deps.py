from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from core.security import verify_token
from core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login", auto_error=False)

async def get_current_user(token: Optional[str] = Depends(oauth2_scheme)):
    """
    Dependência para obter o usuário atual. 
    Se BYPASS_AUTH estiver habilitado, permite acesso sem token (apenas para dev local).
    """
    if settings.BYPASS_AUTH:
        return {"sub": "developer", "name": "Dev User"}
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Autenticação necessária para acessar este recurso",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    user_data = verify_token(token)
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_data
