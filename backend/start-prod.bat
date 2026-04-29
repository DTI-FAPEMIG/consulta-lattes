@echo off
echo ==============================================
echo Iniciando BFF Lattes em modo de Producao...
echo ==============================================
echo .
echo Essa execucao utilizara o Uvicorn puro voltado para
echo multiplas sessoes (workers) e sem a ferramenta reload,
echo evitando que a Azure sobrecarregue em leitura de arquivos.
echo .

:: Descomente se for rodar local via venv ativado pelo bat
:: call venv\Scripts\activate

uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
