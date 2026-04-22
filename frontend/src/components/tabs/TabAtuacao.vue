<script setup>
import { Briefcase, ChevronRight } from 'lucide-vue-next'
import { toArray } from '../../../helpers'
import { computed } from 'vue'

const props = defineProps({
  atuacoes: Array
})

// Filtrar atuações: remover revisores de periódico, revisores de fomento, comitê assessor
const atuacoesFiltradas = computed(() => {
  const filtradas = props.atuacoes.filter(atuacao => {
    const vinculos = toArray(atuacao['VINCULOS'])
    const algumVinculoRelevante = vinculos.some(v => {
      const outroVinculo = (v['OUTRO-VINCULO-INFORMADO'] || '').toLowerCase()
      return !outroVinculo.includes('revisor de peri') && 
             !outroVinculo.includes('revisor de projeto de fomento') &&
             !outroVinculo.includes('membro de comit')
    })
    return vinculos.length === 0 || algumVinculoRelevante
  })

  // Ordena cada atuação pelo ano do seu vínculo mais recente
  return [...filtradas].sort((a, b) => {
    const getMaxAno = (atuacao) => {
      const anos = toArray(atuacao['VINCULOS']).map(v => parseInt(v['ANO-FIM']) || parseInt(v['ANO-INICIO']) || 0)
      return Math.max(...anos, 0)
    }
    return getMaxAno(b) - getMaxAno(a)
  })
})

const sortVinculos = (vinculos) => {
  return [...toArray(vinculos)].sort((a, b) => {
    const anoA = parseInt(a['ANO-INICIO']) || 0
    const anoB = parseInt(b['ANO-INICIO']) || 0
    return anoB - anoA
  })
}

</script>

<template>
  <div class="space-y-6 animate-in">
    <h3 class="text-lg font-bold flex items-center gap-2 mb-4"><Briefcase class="text-blue-500" :size="20"/> Atuação Profissional</h3>
    <div class="grid gap-5">
      <div v-for="(atuacao, idx) in atuacoesFiltradas" :key="idx" class="bg-white border border-slate-200 rounded-2xl p-5 md:p-6 shadow-sm">
        <h4 class="text-lg font-bold mb-3 border-b pb-3 text-slate-800">{{ atuacao['NOME-INSTITUICAO'] }}</h4>
        <div class="space-y-2">
          <div v-for="(vinculo, vIdx) in sortVinculos(atuacao['VINCULOS']).filter(v => {
            const outro = (v['OUTRO-VINCULO-INFORMADO'] || '').toLowerCase()
            return !outro.includes('revisor de peri') && !outro.includes('revisor de projeto de fomento') && !outro.includes('membro de comit')
          })" :key="'v-'+vIdx" class="bg-slate-50 p-3 rounded-xl border border-slate-100 flex gap-3 text-sm">
            <ChevronRight class="shrink-0 text-blue-400 mt-0.5" :size="16" />
            <div class="w-full">
              <div class="flex flex-wrap justify-between gap-2">
                <p class="font-bold text-slate-700">{{ 
                  (['LIVRE','N/A','NA',''].includes((vinculo['OUTRO-VINCULO-INFORMADO'] || '').trim().toUpperCase()) 
                    ? (['LIVRE','N/A','NA',''].includes((vinculo['TIPO-DE-VINCULO'] || '').trim().toUpperCase()) ? 'Vínculo' : vinculo['TIPO-DE-VINCULO']) 
                    : vinculo['OUTRO-VINCULO-INFORMADO']) 
                }}</p>
                <span class="text-xs font-bold text-slate-500 bg-white px-2 py-0.5 rounded border border-slate-100">{{ vinculo['ANO-INICIO'] }} - {{ vinculo['ANO-FIM'] || 'Atual' }}</span>
              </div>
              <p class="text-slate-600 mt-0.5" v-if="vinculo['ENQUADRAMENTO-FUNCIONAL'] && !['LIVRE','N/A','NA'].includes(vinculo['ENQUADRAMENTO-FUNCIONAL'].trim().toUpperCase())">Enquadramento: {{ vinculo['ENQUADRAMENTO-FUNCIONAL'] }}</p>
              <p class="text-slate-600 mt-0.5" v-else-if="vinculo['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO'] && !['LIVRE','N/A','NA'].includes(vinculo['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO'].trim().toUpperCase())">{{ vinculo['OUTRO-ENQUADRAMENTO-FUNCIONAL-INFORMADO'] }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="!atuacoesFiltradas.length" class="text-slate-500 italic p-6 text-center border border-dashed rounded-xl">Sem histórico profissional detalhado.</div>
  </div>
</template>