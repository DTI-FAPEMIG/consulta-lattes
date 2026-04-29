import jwt
from fastapi import HTTPException
from core.config import settings

def verify_token(token: str):
    """
    Decodifica o JWT token e verifica a validade.
    No BFF, apenas checamos a autenticidade verificando com a chave e também expiração.
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido ou malformado.")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Erro de autenticação: {str(e)}")
