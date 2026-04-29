import jwt
import datetime
import os
import sys

# Adiciona o diretório atual no path pra importar o config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from core.config import settings

def gerar_token():
    payload = {
        "sub": "admin_sistema_x",
        "role": "external_service",
        "name": "Sistema Principal da Empresa",
        # Validade de 24 horas para facilitar seu teste local
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24)
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    print("==============================================")
    print("🔑 GENERATED TEST JWT TOKEN")
    print("==============================================")
    print(f"\n{token}\n")
    print("Cole esse token no cabeçalho Authorization ou no botão 'Authorize' do Swagger (http://localhost:8000/docs).")

if __name__ == "__main__":
    gerar_token()
