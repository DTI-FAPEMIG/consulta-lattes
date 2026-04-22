from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List
import pandas as pd
import io

from services.lattes_service import LattesService
from api.deps import get_current_user # Assumindo que get_current_user está em api/deps.py

router = APIRouter()

@router.get("/resume/{id_lattes}")
async def get_lattes_resume(id_lattes: str, user: dict = Depends(get_current_user)):
    """
    Retorna o currículo Lattes completo para um dado ID.
    """
    resume = LattesService.get_complete_resume(id_lattes)
    if resume.get("erro"):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=resume["detalhe"])
    return resume

@router.post("/compare/download-xlsx")
async def download_comparison_xlsx(
    lattes_ids: List[str], 
    user: dict = Depends(get_current_user)
):
    """
    Gera e baixa um arquivo XLSX com os dados de comparação de múltiplos currículos Lattes.
    """
    comparison_data = []
    
    for id_lattes in lattes_ids:
        resume = LattesService.get_complete_resume(id_lattes)
        if resume.get("erro"):
            # Se um currículo não for encontrado, podemos pular ou retornar um erro
            # Por simplicidade, vamos pular e registrar um aviso.
            print(f"Aviso: Currículo Lattes {id_lattes} não encontrado ou com erro: {resume['detalhe']}")
            continue
        
        # Extrair as métricas relevantes para a comparação
        # Esta parte deve espelhar a lógica de `handleAdicionarComparacao` no frontend
        dados_gerais = resume["dados"].get("DADOS-GERAIS", {})
        metricas = resume.get("metricas", {}) 

        resumo_cv = {
            "ID Lattes": id_lattes,
            "Nome Completo": dados_gerais.get("NOME-COMPLETO", "Não informado"),
            **metricas 
        }
        comparison_data.append(resumo_cv)

    if not comparison_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Nenhum currículo encontrado para comparação.")

    df = pd.DataFrame(comparison_data)

    # Remover colunas com "(recorte)" no título ou "_recorte" no nome da coluna, conforme solicitado
    cols_to_keep = [col for col in df.columns if "(recorte)" not in str(col) and "_recorte" not in str(col)]
    df = df[cols_to_keep]

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Comparacao Lattes')
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=comparacao_lattes.xlsx"}
    )