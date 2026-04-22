import zeep
import zipfile
import io
import lxml.etree as ET
import sys
import os
from cachetools import TTLCache, cached
from core.config import settings

# Caches para otimização de RAM (Evita CPU e SOAP reduntantes)
short_resume_cache = TTLCache(maxsize=settings.LATTES_CACHE_MAX_SIZE, ttl=settings.LATTES_CACHE_TTL_SECONDS)
complete_resume_cache = TTLCache(maxsize=settings.LATTES_CACHE_MAX_SIZE, ttl=settings.LATTES_CACHE_TTL_SECONDS)

class LattesService:
    WSDL_URL = "http://servicosweb.cnpq.br/srvcurriculo/WSCurriculo?wsdl"

    @classmethod
    @cached(cache=short_resume_cache, key=lambda cls, id_lattes: id_lattes)
    def get_short_resume(cls, id_lattes: str):
        try:
            client = zeep.Client(wsdl=cls.WSDL_URL)
            # O retorno é o conteúdo binário do ZIP
            zip_bin = client.service.getCurriculoCompactado(id=id_lattes)

            if not zip_bin:
                return {"erro": "NOT_FOUND"}

            # Descompactação
            with zipfile.ZipFile(io.BytesIO(zip_bin)) as z:
                xml_name = z.namelist()[0]
                with z.open(xml_name) as f:
                    xml_content = f.read()

            # Parsing com suporte a ISO-8859-1 (Padrão CNPq)
            parser = ET.XMLParser(recover=True, encoding='ISO-8859-1')
            root = ET.fromstring(xml_content, parser=parser)

            # Verificação de Erro de IP (Tag <MENSAGEM>)
            if root.tag == "MENSAGEM":
                erro_node = root.find("ERRO")
                msg = erro_node.text if erro_node is not None else "Erro desconhecido"
                return {"erro": "IP_DENIED", "detalhe": msg}

            # Extração de Dados do Currículo
            dados_gerais = root.find("DADOS-GERAIS")
            if dados_gerais is None:
                return {"erro": "NOT_FOUND"}

            return {
                "id": id_lattes,
                "nome": dados_gerais.get("NOME-COMPLETO"),
                "formacao": {
                    "mestrados": len(root.xpath("//MESTRADO")),
                    "doutorados": len(root.xpath("//DOUTORADO")),
                    "graduacoes": len(root.xpath("//GRADUACAO")),
                    "especializacoes": len(root.xpath("//ESPECIALIZACAO"))
                },
                "atualizacao": root.get("DATA-ATUALIZACAO")
            }

        except Exception as e:
            return {"erro": "INTERNAL_ERROR", "detalhe": str(e)}

    @classmethod
    # Temporariamente desabilitando cache para garantir atualização das métricas
    # @cached(cache=complete_resume_cache, key=lambda cls, id_lattes: id_lattes)
    def get_complete_resume(cls, id_lattes: str):
        try:
            client = zeep.Client(wsdl=cls.WSDL_URL)
            # O retorno é o conteúdo binário do ZIP
            zip_bin = client.service.getCurriculoCompactado(id=id_lattes)
            
            if not zip_bin: return {"erro": "NOT_FOUND"}

            with zipfile.ZipFile(io.BytesIO(zip_bin)) as z:
                with z.open(z.namelist()[0]) as f:
                    xml_content = f.read()

            parser = ET.XMLParser(recover=True, encoding='ISO-8859-1')
            root = ET.fromstring(xml_content, parser=parser)

            if root.tag == "MENSAGEM":
                return {"erro": "API_ERROR", "detalhe": root.findtext("ERRO")}
            
            # Converte para dicionário
            resume_data = cls._xml_to_dict(root)

            # Extrai métricas principais
            metricas = cls._extract_metrics(root)
            resume_data["metricas"] = metricas

            # Aplica pós-processamento
            processed_data = cls._post_process_resume_data(resume_data)
            if processed_data:
                resume_data = processed_data

            return {
                "id_solicitado": id_lattes,
                "dados": resume_data,
                "metricas": metricas
            }

        except Exception as e:
            return {"erro": "INTERNAL_ERROR", "detalhe": str(e)}

    @classmethod
    def _extract_metrics(cls, root):
        """Extrai um conjunto de métricas completo para o quadro comparativo."""
        metrics = {}
        
        # 1. Dados Básicos & Heurística PQ
        dados_gerais = root.find("DADOS-GERAIS")
        nome_pesquisador = dados_gerais.get("NOME-COMPLETO") if dados_gerais is not None else ""
        resumo_cv = root.xpath("//OUTROS-DADOS-INDIVIDUAIS/@TEXTO-RESUMO-CV-RH")
        resumo_texto = resumo_cv[0].upper() if resumo_cv else ""
        
        metrics["nivel_atual_bolsa_pq"] = "Não identificada"
        metrics["data_primeira_bolsa_pq_cnpq"] = "Não identificada"
        if "BOLSISTA DE PRODUTIVIDADE" in resumo_texto:
            import re
            match_nivel = re.search(r"N[íI]VEL\s+([12][ABCD]?)", resumo_texto)
            if match_nivel:
                metrics["nivel_atual_bolsa_pq"] = match_nivel.group(1)
            
            match_ano = re.search(r"DESDE\s+(\d{4})", resumo_texto)
            if match_ano:
                metrics["data_primeira_bolsa_pq_cnpq"] = match_ano.group(1)

        # 2. Formação Acadêmica - Ano término Doutorado (Reforçado)
        anos_doutorado = []
        # Tenta buscar via tag DOUTORADO
        for d in root.xpath("//DOUTORADO"):
            # Pega todos os atributos que contenham ANO e CONCLUSAO
            attrs = d.xpath(".//@*[contains(name(), 'ANO') and contains(name(), 'CONCLUSAO')]")
            if not attrs: attrs = d.xpath(".//@ANO")
            
            for val in attrs:
                if str(val).isdigit() and len(str(val)) == 4:
                    anos_doutorado.append(int(val))
                    break # Encontrou um ano no bloco, pula para o próximo PhD
        
        # Pega o menor ano de conclusão (primeiro doutorado)
        metrics["ano_termino_primeiro_doutorado"] = min(anos_doutorado) if anos_doutorado else None
        
        # 3. Pós-Doc Exterior
        pos_docs = root.xpath("//POS-DOUTORADO")
        pos_doc_exterior = "Não"
        for p in pos_docs:
            pais = p.xpath("./DADOS-BASICOS-DO-POS-DOUTORADO/@PAIS")
            if pais and pais[0].upper() not in ["BRASIL", "BRAZIL"]:
                pos_doc_exterior = "Sim"
                break
        metrics["treinamento_previo_posdoc_exterior"] = pos_doc_exterior

        # 4. Produção Bibliográfica (Artigos)
        artigos = root.xpath("//ARTIGO-PUBLICADO")
        metrics["num_artigos_publicados_periodicos"] = len(artigos)
        
        a10, a11_19, a20_mais = 0, 0, 0
        primeiro_autor = 0
        for art in artigos:
            autores = art.xpath("./AUTORES")
            num_autores = len(autores)
            if num_autores <= 10: a10 += 1
            elif 11 <= num_autores <= 19: a11_19 += 1
            else: a20_mais += 1
            
            p_autor = art.xpath("./AUTORES[@ORDEM-DE-INTEGRACAO='1']/@NOME-COMPLETO-DO-AUTOR")
            if not p_autor: p_autor = art.xpath("./AUTORES[1]/@NOME-COMPLETO-DO-AUTOR")
            
            if p_autor and cls._names_match(nome_pesquisador, p_autor[0]):
                primeiro_autor += 1
                
        metrics["num_artigos_10_menos_autores"] = a10
        metrics["num_artigos_11_a_19_autores"] = a11_19
        metrics["num_artigos_20_mais_autores"] = a20_mais
        metrics["num_artigos_primeiro_autor"] = primeiro_autor
        
        current_year = 2026
        if metrics["ano_termino_primeiro_doutorado"]:
            anos_carreira = (current_year - metrics["ano_termino_primeiro_doutorado"]) + 1
            metrics["media_artigos_publicados_periodicos"] = round(len(artigos) / max(1, anos_carreira), 2)
        else:
            metrics["media_artigos_publicados_periodicos"] = 0

        # ... demais métricas (abreviadas para brevidade mas preservadas no arquivo real)
        metrics["num_livros"] = len(root.xpath("//LIVRO-PUBLICADO-OU-ORGANIZADO"))
        metrics["num_obras_organizadas"] = len(root.xpath("//LIVRO-PUBLICADO-OU-ORGANIZADO[contains(@TIPO, 'ORGANIZADOR') or contains(@TIPO, 'EDICAO')]"))
        metrics["num_capitulos_livros"] = len(root.xpath("//CAPITULO-DE-LIVRO-PUBLICADO"))
        
        # Orientações (Fix individual tags)
        metrics["num_orientacoes_ic_concluidas_total"] = len(root.xpath("//OUTRA-ORIENTACAO-CONCLUIDA[DADOS-BASICOS-DE-OUTRA-ORIENTACAO-CONCLUIDA/@NATUREZA='INICIACAO_CIENTIFICA']"))
        metrics["num_orientacoes_mestrado_concluidas_total"] = len(root.xpath("//ORIENTACAO-CONCLUIDA-PARA-MESTRADO[DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO/@TIPO-DE-ORIENTACAO='ORIENTADOR_PRINCIPAL']"))
        metrics["num_orientacoes_doutorado_concluidas_total"] = len(root.xpath("//ORIENTACAO-CONCLUIDA-PARA-DOUTORADO[DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO/@TIPO-DE-ORIENTACAO='ORIENTADOR_PRINCIPAL']"))
        metrics["num_supervisao_posdoc_concluidas_total"] = len(root.xpath("//ORIENTACAO-CONCLUIDA-PARA-POS-DOUTORADO"))
        
        metrics["num_coorientacoes_mestrado_concluidas_total"] = len(root.xpath("//ORIENTACAO-CONCLUIDA-PARA-MESTRADO[DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-MESTRADO/@TIPO-DE-ORIENTACAO='CO_ORIENTADOR']"))
        metrics["num_coorientacoes_doutorado_concluidas_total"] = len(root.xpath("//ORIENTACAO-CONCLUIDA-PARA-DOUTORADO[DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO/@TIPO-DE-ORIENTACAO='CO_ORIENTADOR']"))

        metrics["num_orientacoes_ic_andamento"] = len(root.xpath("//ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA"))
        metrics["num_orientacoes_mestrado_andamento"] = len(root.xpath("//ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO[DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO/@TIPO-DE-ORIENTACAO='ORIENTADOR_PRINCIPAL']"))
        metrics["num_orientacoes_doutorado_andamento"] = len(root.xpath("//ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO[DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO/@TIPO-DE-ORIENTACAO='ORIENTADOR_PRINCIPAL']"))
        metrics["num_supervisao_posdoc_andamento"] = len(root.xpath("//ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO"))
        
        metrics["num_coorientacoes_mestrado_andamento"] = len(root.xpath("//ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO[DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO/@TIPO-DE-ORIENTACAO='CO_ORIENTADOR']"))
        metrics["num_coorientacoes_doutorado_andamento"] = len(root.xpath("//ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO[DADOS-BASICOS-DA-ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO/@TIPO-DE-ORIENTACAO='CO_ORIENTADOR']"))

        metrics["num_patentes_registradas"] = len(root.xpath("//PATENTE"))
        metrics["num_trabalhos_completos_eventos"] = len(root.xpath("//TRABALHO-EM-EVENTOS[DADOS-BASICOS-DO-TRABALHO/@NATUREZA='COMPLETO']"))
        metrics["num_eventos_organizador"] = len(root.xpath("//ORGANIZACAO-DE-EVENTO"))
        metrics["num_eventos_participante_convidado"] = len(root.xpath("//PARTICIPACAO-EM-EVENTO-CONGRESSO[.//DADOS-BASICOS-DA-PARTICIPACAO-EM-EVENTO-CONGRESSO/@FORMA-DE-PARTICIPACAO='CONVIDADO' or .//DADOS-BASICOS-DA-PARTICIPACAO-EM-EVENTO-CONGRESSO/@TIPO-DE-PARTICIPACAO='CONVIDADO']"))
        
        metrics["num_premios_titulos_honorificos"] = len(root.xpath("//PREMIO-TITULO"))
        metrics["lider_grupos_pesquisa_cnpq"] = cls._count_group_leadership(root)
        metrics["num_producoes_educacao_popularizacao_cet"] = len(root.xpath("//*[@FLAG-DIVULGACAO-CIENTIFICA='SIM']"))
        metrics["num_periodicos_membro_corpo_editorial_atual"] = len(root.xpath("//EDITORIA-DE-PERIODICO[not(@ANO-FIM) or @ANO-FIM='']"))
        metrics["num_comites_assessoramento"] = len(root.xpath("//CONSELHO-DIRETIVO-OU-CONSULTIVO") + root.xpath("//COMITE-DE-ASSESSORAMENTO"))
        metrics["num_inovacoes_projetos_empresas"] = len(root.xpath("//PROJETO-DE-PESQUISA[contains(@NATUREZA, 'DESENVOLVIMENTO') or contains(@NATUREZA, 'INOVACAO')]"))
        metrics["num_projetos_certificados_lattes"] = len(root.xpath("//PROJETO-DE-PESQUISA[@CERTIFICADO-PELA-INSTITUICAO='SIM']"))

        return metrics

    @classmethod
    def _names_match(cls, name1, name2):
        if not name1 or not name2: return False
        n1 = "".join(name1.upper().split())
        n2 = "".join(name2.upper().split())
        return n1 == n2

    @classmethod
    def _sort_by_year(cls, items, year_attr_candidates):
        if not isinstance(items, list): return items
        def get_year(item):
            for attr in year_attr_candidates:
                val = item.get(attr)
                if val and val.isdigit() and len(val) == 4: return int(val)
            return 0
        return sorted(items, key=get_year, reverse=True)

    @classmethod
    def _post_process_resume_data(cls, data):
        if not data: return data
        if "FORMACAO-ACADEMICA-TITULACAO" in data:
            formacao = data["FORMACAO-ACADEMICA-TITULACAO"]
            for tag in ["GRADUACAO", "MESTRADO", "DOUTORADO", "ESPECIALIZACAO"]:
                if tag in formacao:
                    items = formacao[tag]
                    # Mantém no lugar mas ordena
                    if isinstance(items, list):
                        formacao[tag] = cls._sort_by_year(items, ["ANO-DE-CONCLUSAO", "ANO-DE-INICIO"])
        return data

    @classmethod
    def _count_group_leadership(cls, root_element):
        count = len(root_element.xpath("//LIDERANCA-DE-GRUPO-DE-PESQUISA"))
        roles = root_element.xpath("//ATUACAO-PROFISSIONAL//ATIVIDADES-DE-DIRECAO-E-ADMINISTRACAO//DADOS-BASICOS-DE-DIRECAO-E-ADMINISTRACAO/@NOME-DO-CARGO")
        for r in roles:
            if "LIDER" in r.upper() or "COORDENADOR" in r.upper(): count += 1
        return count

    @classmethod
    def _xml_to_dict(cls, node):
        res = {**node.attrib}
        for child in node:
            child_data = cls._xml_to_dict(child)
            tag = child.tag
            if tag not in res: res[tag] = child_data
            else:
                if not isinstance(res[tag], list): res[tag] = [res[tag]]
                res[tag].append(child_data)
        return res
