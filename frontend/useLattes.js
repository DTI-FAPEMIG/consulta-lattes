import { ref, computed } from 'vue'
import axios from 'axios'
import { toArray } from './helpers'

// Interceptador de Requisição (Pega o token JWT do LocalStorage após o usuário logar)
axios.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptador de Resposta (Vigia se o token venceu para tentar o Refresh nos bastidores)
axios.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    const token = localStorage.getItem('access_token');

    // Se o FastAPI recusar (401 - Vencido) e tínhamos um token e for a primeira vez que tenta...
    if (error.response && error.response.status === 401 && token && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        console.log("Tentando renovar token expirado...");
        
        // Chamada oficial de Sliding Token (Usando axios puro isolado para não dar loop)
        const axiosRefresh = axios.create();
        const refreshResponse = await axiosRefresh.post(
          'https://api-pr-2166.plataformaevandomirra.fapemig.br/api/auth/refresh',
          {}, 
          {
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json',
              'Authorization': `Bearer ${token}`
            }
          }
        );

        const newToken = refreshResponse.data.token || refreshResponse.data.access_token;
        if (!newToken) throw new Error("API não devolveu o novo passe.");

        localStorage.setItem('access_token', newToken);
        originalRequest.headers.Authorization = `Bearer ${newToken}`;
        
        return axios(originalRequest); 

      } catch (refreshErr) {
        console.warn("Token irrecuperável. Limpando sessão temporária.");
        localStorage.removeItem('access_token');
        // window.location.reload(); // Removido para evitar reload infinito em dev
      }
    }
    return Promise.reject(error);
  }
);

export function useLattes() {
  const idLattes = ref('')
  const loading = ref(false)
  const resultado = ref(null)
  const erro = ref(null)

  const buscarCurriculo = async () => {
    if (!idLattes.value) return
    
    loading.value = true
    erro.value = null
    resultado.value = null

    try {
      const apiBase = import.meta.env.VITE_API_URL || 'http://localhost:8000'
      const response = await axios.get(`${apiBase}/api/v1/resume/${idLattes.value}`)
      
      let responseData = response.data
      if (typeof responseData === 'string') {
        try {
          responseData = JSON.parse(responseData)
        } catch (parseError) {
          console.error("Erro ao converter retorno da API para JSON.", parseError)
        }
      }
      
      resultado.value = responseData
    } catch (err) {
      if (err.response) {
        if (err.response.status === 403) erro.value = { tipo: 'IP', msg: 'Acesso negado no CNPq.' }
        else if (err.response.status === 404) erro.value = { tipo: 'NOT_FOUND', msg: 'Currículo não encontrado.' }
        else erro.value = { tipo: 'ERRO', msg: err.response.data?.detail || 'Erro interno do servidor.' }
      } else {
        erro.value = { tipo: 'ERRO', msg: 'Falha de conexão com o backend.' }
      }
    } finally {
      loading.value = false
    }
  }

  const safeData = computed(() => resultado.value?.dados || resultado.value || {})
  const dadosGerais = computed(() => safeData.value['DADOS-GERAIS'] || {})
  const enderecoProfissional = computed(() => dadosGerais.value['ENDERECO']?.['ENDERECO-PROFISSIONAL'] || {})
  const areasAtuacao = computed(() => toArray(dadosGerais.value['AREAS-DE-ATUACAO']?.['AREA-DE-ATUACAO']))
  const formacao = computed(() => dadosGerais.value['FORMACAO-ACADEMICA-TITULACAO'] || {})
  const atuacoes = computed(() => toArray(dadosGerais.value['ATUACOES-PROFISSIONAIS']?.['ATUACAO-PROFISSIONAL']))
  const idiomas = computed(() => toArray(dadosGerais.value['IDIOMAS']?.['IDIOMA']))
  const premios = computed(() => toArray(dadosGerais.value['PREMIOS-TITULOS']?.['PREMIO-TITULO']))
  const producaoBiblio = computed(() => safeData.value['PRODUCAO-BIBLIOGRAFICA'] || {})
  const artigos = computed(() => toArray(producaoBiblio.value['ARTIGOS-PUBLICADOS']?.['ARTIGO-PUBLICADO']))
  const eventos = computed(() => toArray(producaoBiblio.value['TRABALHOS-EM-EVENTOS']?.['TRABALHO-EM-EVENTOS']))
  const metricas = computed(() => resultado.value?.metricas || {})

  // Capítulos de livros publicados
  const capitulosLivros = computed(() => toArray(producaoBiblio.value['LIVROS-E-CAPITULOS']?.['CAPITULOS-DE-LIVROS-PUBLICADOS']?.['CAPITULO-DE-LIVRO-PUBLICADO']))

  // Livros publicados/organizados
  const livros = computed(() => toArray(producaoBiblio.value['LIVROS-E-CAPITULOS']?.['LIVROS-PUBLICADOS-OU-ORGANIZADOS']?.['LIVRO-PUBLICADO-OU-ORGANIZADO']))

  // Trabalhos completos publicados em anais de congressos
  const trabalhosAnais = computed(() => {
    return eventos.value.filter(ev => {
      const natureza = ev['DADOS-BASICOS-DO-TRABALHO']?.['NATUREZA'] || ''
      return natureza === 'COMPLETO'
    })
  })

  // Patentes e Registros
  const patentes = computed(() => toArray(safeData.value['PRODUCAO-TECNICA']?.['PATENTE']))

  // Orientações concluídas
  const orientacoesConcluidas = computed(() => safeData.value['OUTRA-PRODUCAO']?.['ORIENTACOES-CONCLUIDAS'] || {})
  
  // Orientações em andamento
  const orientacoesAndamento = computed(() => dadosGerais.value['ORIENTACOES-EM-ANDAMENTO'] || safeData.value['DADOS-COMPLEMENTARES']?.['ORIENTACOES-EM-ANDAMENTO'] || {})

  // Orientações unificadas
  const orientacoes = computed(() => ({
    doutoradoConcluido: toArray(orientacoesConcluidas.value['ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO']),
    mestradoConcluido: toArray(orientacoesConcluidas.value['ORIENTACOES-CONCLUIDAS-PARA-MESTRADO']),
    posDocConcluido: toArray(orientacoesConcluidas.value['ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO']),
    icConcluida: toArray(orientacoesConcluidas.value['OUTRAS-ORIENTACOES-CONCLUIDAS']).filter(o => {
      const db = o[`DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS`] || o['DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS'] || {}
      return db['NATUREZA'] === 'INICIACAO_CIENTIFICA'
    }),
    doutoradoAndamento: toArray(orientacoesAndamento.value['ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO']),
    mestradoAndamento: toArray(orientacoesAndamento.value['ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO']),
    posDocAndamento: toArray(orientacoesAndamento.value['ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO']),
    icAndamento: toArray(orientacoesAndamento.value['ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA']),
  }))

  return {
    idLattes, loading, resultado, erro, buscarCurriculo, safeData, metricas, dadosGerais, 
    enderecoProfissional, areasAtuacao, formacao, atuacoes, idiomas, premios, artigos, eventos,
    capitulosLivros, livros, trabalhosAnais, patentes, orientacoes
  }
}