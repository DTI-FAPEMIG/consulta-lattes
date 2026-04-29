<script setup>
import { ref, computed } from 'vue'
import { Trash2, Maximize2, X, ChevronLeft, ChevronRight, Download, ChevronUp, ChevronDown } from 'lucide-vue-next'

const props = defineProps({
  listaCurriculos: Array
})

defineEmits(['remover'])

const isExpanded = ref(false)
const scrollContainer = ref(null)

// Ordenação
const sortKey = ref(null)
const sortDir = ref('desc') // 'asc' | 'desc'

const toggleSort = (key) => {
  if (sortKey.value === key) {
    sortDir.value = sortDir.value === 'desc' ? 'asc' : 'desc'
  } else {
    sortKey.value = key
    sortDir.value = 'desc'
  }
}

const sortedCurriculos = computed(() => {
  if (!sortKey.value) return props.listaCurriculos
  return [...props.listaCurriculos].sort((a, b) => {
    const va = a[sortKey.value] ?? ''
    const vb = b[sortKey.value] ?? ''
    // Desempate alfabético por nome
    if (va === vb) return (a.nome || '').localeCompare(b.nome || '', 'pt-BR')
    if (typeof va === 'number' && typeof vb === 'number') {
      return sortDir.value === 'desc' ? vb - va : va - vb
    }
    const cmp = String(va).localeCompare(String(vb), 'pt-BR', { numeric: true })
    return sortDir.value === 'desc' ? -cmp : cmp
  })
})

const scrollTable = (direction) => {
  if (!scrollContainer.value) return
  const amount = window.innerWidth * 0.35
  scrollContainer.value.scrollBy({ left: direction === 'left' ? -amount : amount, behavior: 'smooth' })
}

// Download XLSX via SheetJS (carregado via CDN dinâmico para não precisar instalar)
const downloadXLSX = async () => {
  // Carrega XLSX dinamicamente se não estiver carregado
  if (!window.XLSX) {
    await new Promise((resolve, reject) => {
      const script = document.createElement('script')
      script.src = 'https://cdn.sheetjs.com/xlsx-0.20.2/package/dist/xlsx.full.min.js'
      script.onload = resolve
      script.onerror = reject
      document.head.appendChild(script)
    })
  }
  const XLSX = window.XLSX

  // Monta os dados: primeira linha = cabeçalhos, demais = linhas de currículos
  const headers = ['Pesquisador', 'ID Lattes', ...metricLabels.map(m => m.label)]
  const rows = props.listaCurriculos.map(cv => [
    cv.nome,
    cv.idLattes,
    ...metricLabels.map(m => cv[m.key] ?? '')
  ])

  const ws = XLSX.utils.aoa_to_sheet([headers, ...rows])
  const wb = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(wb, ws, 'Comparativo')
  XLSX.writeFile(wb, 'comparativo_lattes.xlsx')
}

const metricLabels = [
  { key: 'ano_termino_primeiro_doutorado', label: 'Ano de término do\ndoutorado' },
  { key: 'data_primeira_bolsa_pq_cnpq', label: 'Data da primeira\nbolsa PQ no CNPq' },
  { key: 'lider_grupos_pesquisa_cnpq', label: 'Líder de grupos de\npesquisa do CNPq' },
  { key: 'treinamento_previo_posdoc_exterior', label: 'Pós-doutorado\nno exterior' },
  { key: 'num_producoes_educacao_popularizacao_cet', label: 'Produções para\npopularização C&T' },
  { key: 'num_periodicos_membro_corpo_editorial_atual', label: 'Membro de corpo\neditorial (Atual)' },
  { key: 'num_artigos_publicados_periodicos', label: 'Artigos publicados\nem periódicos' },
  { key: 'num_artigos_10_menos_autores', label: 'Artigos com\n≤10 autores' },
  { key: 'num_artigos_11_a_19_autores', label: 'Artigos com\n11–19 autores' },
  { key: 'num_artigos_20_mais_autores', label: 'Artigos com\n≥20 autores' },
  { key: 'num_artigos_primeiro_autor', label: 'Artigos como\n1º autor' },
  { key: 'media_artigos_publicados_periodicos', label: 'Média de artigos\npublicados' },
  { key: 'num_orientacoes_ic_concluidas_total', label: 'Orientações IC\nconcluídas' },
  { key: 'num_orientacoes_ic_andamento', label: 'Orientações IC\nem andamento' },
  { key: 'num_orientacoes_mestrado_concluidas_total', label: 'Orientações mestrado\nconcluídas' },
  { key: 'num_orientacoes_mestrado_andamento', label: 'Orientações mestrado\nem andamento' },
  { key: 'num_orientacoes_doutorado_concluidas_total', label: 'Orientações doutorado\nconcluídas' },
  { key: 'num_orientacoes_doutorado_andamento', label: 'Orientações doutorado\nem andamento' },
  { key: 'num_supervisao_posdoc_concluidas_total', label: 'Supervisões pós-doc\nconcluídas' },
  { key: 'num_supervisao_posdoc_andamento', label: 'Supervisões pós-doc\nem andamento' },
  { key: 'num_trabalhos_completos_eventos', label: 'Trabalhos completos\nem eventos' },
  { key: 'num_livros', label: 'Nº de\nlivros' },
  { key: 'num_obras_organizadas', label: 'Nº de obras\norganizadas' },
  { key: 'num_capitulos_livros', label: 'Capítulos de\nlivros publicados' },
  { key: 'num_patentes_registradas', label: 'Patentes\nregistradas' },
  { key: 'num_eventos_organizador', label: 'Eventos como\norganizador' },
  { key: 'num_eventos_participante_convidado', label: 'Participante\nconvidado' },
  { key: 'num_comites_assessoramento', label: 'Comitês de\nassessoramento' },
  { key: 'num_inovacoes_projetos_empresas', label: 'Inovações por\nprojetos empresas' },
  { key: 'num_premios_titulos_honorificos', label: 'Prêmios e títulos\nhonoríficos' },
  { key: 'num_projetos_certificados_lattes', label: 'Projetos certificados\nno Lattes' },
  { key: 'nivel_atual_bolsa_pq', label: 'Nível atual\nda bolsa PQ' },
  { key: 'num_coorientacoes_mestrado_andamento', label: 'Co-orientações mestrado\nem andamento' },
  { key: 'num_coorientacoes_doutorado_andamento', label: 'Co-orientações doutorado\nem andamento' },
  { key: 'num_coorientacoes_mestrado_concluidas_total', label: 'Co-orientações mestrado\nconcluídas' },
  { key: 'num_coorientacoes_doutorado_concluidas_total', label: 'Co-orientações doutorado\nconcluídas' },
]
</script>

<template>
  <div class="space-y-6 animate-in w-full min-w-0 max-w-full">
    
    <div class="flex items-center justify-between mb-4">
      <h3 class="text-lg font-bold flex items-center gap-2">
        📊 Quadro Comparativo
      </h3>
      <div class="flex gap-3 items-center flex-wrap">
        
        <div v-if="listaCurriculos.length > 0 && !isExpanded" class="hidden md:flex items-center bg-white border border-slate-200 rounded-lg shadow-sm">
          <button @click="scrollTable('left')" class="p-1.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 transition-colors rounded-l-lg border-r border-slate-100" title="Rolar Esquerda"><ChevronLeft :size="16" /></button>
          <button @click="scrollTable('right')" class="p-1.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 transition-colors rounded-r-lg" title="Rolar Direita"><ChevronRight :size="16" /></button>
        </div>

        <span class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-xs font-bold">
          {{ listaCurriculos.length }} currículos
        </span>

        <!-- Botão Download XLSX -->
        <button
          v-if="listaCurriculos.length > 0"
          @click="downloadXLSX"
          class="flex items-center gap-2 text-sm font-bold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 px-3 py-1.5 rounded-lg transition-colors"
          title="Baixar planilha Excel"
        >
          <Download :size="15" /> Baixar .xlsx
        </button>
        
        <button 
          v-if="listaCurriculos.length > 0 && !isExpanded" 
          @click="isExpanded = true"
          class="flex items-center gap-2 text-sm font-bold text-slate-600 bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg transition-colors"
        >
          <Maximize2 :size="16" /> Expandir
        </button>
      </div>
    </div>

    <div v-if="listaCurriculos.length === 0" class="text-slate-500 italic p-6 text-center border border-dashed rounded-xl bg-slate-50">
      Nenhum currículo adicionado para comparação ainda.
    </div>

    <Teleport to="body" :disabled="!isExpanded">
      <div v-if="listaCurriculos.length > 0" :class="isExpanded ? 'fixed inset-0 z-[9999] bg-slate-900/80 backdrop-blur-sm p-4 md:p-8 flex items-center justify-center' : 'w-full block'">
        
        <div :class="isExpanded ? 'bg-white w-full h-full rounded-3xl shadow-2xl flex flex-col overflow-hidden animate-in' : 'w-full bg-white rounded-2xl overflow-hidden border border-slate-200'">
          
          <div v-if="isExpanded" class="p-4 md:p-6 border-b border-slate-200 flex justify-between items-center bg-slate-50 shrink-0">
            <h3 class="text-xl md:text-2xl font-black text-slate-800">Comparação Detalhada</h3>
            
            <div class="flex items-center gap-3">
              <button
                @click="downloadXLSX"
                class="flex items-center gap-2 text-sm font-bold text-emerald-700 bg-emerald-50 hover:bg-emerald-100 border border-emerald-200 px-3 py-2 rounded-xl transition-colors"
              >
                <Download :size="16" /> Baixar .xlsx
              </button>

              <div class="flex items-center bg-white border border-slate-200 rounded-xl shadow-sm">
                <button @click="scrollTable('left')" class="p-2 md:p-2.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 transition-colors rounded-l-xl border-r border-slate-100" title="Rolar Esquerda">
                  <ChevronLeft :size="20" />
                </button>
                <button @click="scrollTable('right')" class="p-2 md:p-2.5 text-slate-400 hover:text-blue-600 hover:bg-blue-50 transition-colors rounded-r-xl" title="Rolar Direita">
                  <ChevronRight :size="20" />
                </button>
              </div>

              <button @click="isExpanded = false" class="p-2 md:p-3 bg-slate-200 hover:bg-red-100 hover:text-red-600 rounded-xl transition-colors" title="Fechar Comparação">
                <X :size="24" />
              </button>
            </div>
          </div>

          <div :class="isExpanded ? 'flex-1 min-h-0 bg-slate-50/50 p-4 md:p-6 flex flex-col' : ''">
            <div ref="scrollContainer" class="w-full overflow-x-auto scrollbar-thin scroll-smooth" :class="isExpanded ? 'flex-1 overflow-y-auto bg-white shadow-sm border border-slate-200 rounded-2xl' : ''">
              
              <table class="w-full border-collapse text-sm text-left relative" :class="isExpanded ? '' : 'bg-white rounded-2xl'">
              
              <thead>
                <tr class="bg-slate-100 border-b border-slate-200">
                  <th class="sticky left-0 z-20 bg-slate-100 w-[62px] min-w-[62px]"></th>
                  <th class="p-4 font-bold text-slate-700 whitespace-nowrap sticky left-[60px] z-30 bg-slate-100 shadow-[1px_0_0_0_#e2e8f0]">Pesquisador</th>
                  <th 
                    v-for="col in metricLabels" 
                    :key="col.key" 
                    class="p-3 font-bold text-slate-700 text-center align-top cursor-pointer select-none hover:bg-slate-200 transition-colors min-w-[130px]"
                    @click="toggleSort(col.key)"
                    :title="'Ordenar por: ' + col.label.replace('\n', ' ')"
                  >
                    <div class="flex flex-col items-center gap-1">
                      <!-- Quebra label na \n em duas linhas -->
                      <span class="leading-tight text-xs text-center" style="white-space: pre-line;">{{ col.label }}</span>
                      <span class="flex items-center text-slate-400">
                        <ChevronUp 
                          :size="12" 
                          :class="sortKey === col.key && sortDir === 'asc' ? 'text-blue-600' : 'text-slate-300'" 
                        />
                        <ChevronDown 
                          :size="12" 
                          :class="sortKey === col.key && sortDir === 'desc' ? 'text-blue-600' : 'text-slate-300'" 
                        />
                      </span>
                    </div>
                  </th>
                </tr>
              </thead>
              
              <tbody>
                <tr v-for="cv in sortedCurriculos" :key="cv.idLattes" class="border-b border-slate-100 hover:bg-slate-50 transition-colors group">
                  
                  <td class="sticky left-0 z-10 bg-white w-[62px] min-w-[62px] text-center group-hover:bg-slate-50 transition-colors">
                    <button @click="$emit('remover', cv.idLattes)" class="inline-flex text-slate-300 hover:text-red-500 hover:bg-red-50 p-2 rounded-xl transition-all" title="Remover da comparação">
                      <Trash2 :size="18" />
                    </button>
                  </td>

                  <td class="p-4 sticky left-[60px] z-20 bg-white shadow-[1px_0_0_0_#f1f5f9] min-w-[280px] max-w-[350px] group-hover:bg-slate-50 transition-colors">
                    <a :href="`https://lattes.cnpq.br/${cv.idLattes}`" target="_blank" rel="noopener noreferrer" class="font-bold text-slate-800 hover:text-blue-700 transition-colors line-clamp-2 leading-tight" title="Abrir Lattes em nova aba">
                      {{ cv.nome }}
                    </a>
                    <p class="text-xs text-slate-500 font-mono mt-1.5">{{ cv.idLattes }}</p>
                  </td>
                  
                  <td v-for="col in metricLabels" :key="col.key" class="p-4 text-center font-medium text-slate-700">
                    <span v-if="cv[col.key] !== undefined && cv[col.key] !== null" class="bg-blue-50 text-blue-700 px-2.5 py-1 rounded-md font-bold">{{ cv[col.key] }}</span>
                    <span v-else class="text-slate-300">-</span>
                  </td>
                </tr>
              </tbody>

            </table>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>