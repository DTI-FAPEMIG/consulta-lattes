<script setup>
import { computed } from 'vue'
import { GraduationCap } from 'lucide-vue-next'
import { toArray } from '../../../helpers'

const props = defineProps({
  formacao: Object
})

// Ordena por ano de conclusão (mais recente primeiro), depois ano de início
const sortFormacao = (lista) =>
  [...lista].sort((a, b) => {
    const anoA = parseInt(a['ANO-DE-CONCLUSAO']) || parseInt(a['ANO-DE-INICIO']) || 0
    const anoB = parseInt(b['ANO-DE-CONCLUSAO']) || parseInt(b['ANO-DE-INICIO']) || 0
    return anoB - anoA
  })

const doutorados = computed(() => sortFormacao(toArray(props.formacao['DOUTORADO'])))
const mestrados = computed(() => sortFormacao(toArray(props.formacao['MESTRADO'])))
const graduacoes = computed(() => sortFormacao(toArray(props.formacao['GRADUACAO'])))
const posDoutorados = computed(() => sortFormacao(toArray(props.formacao['POS-DOUTORADO'])))

const temHistoricoAcademico = computed(() =>
  doutorados.value.length || mestrados.value.length || graduacoes.value.length
)
</script>

<template>
  <div class="space-y-6 animate-in">
    <h3 class="text-lg font-bold flex items-center gap-2 mb-6"><GraduationCap class="text-blue-500" :size="20"/> Histórico Acadêmico</h3>
    
    <div class="space-y-6 ml-2">

      <!-- Doutorado -->
      <div v-for="(item, idx) in doutorados" :key="'doc-'+idx" class="relative pl-8 border-l-2 border-slate-100 pb-2">
        <div class="absolute w-4 h-4 bg-purple-500 border-4 border-white rounded-full -left-[9px] top-1"></div>
        <span class="text-xs font-bold bg-purple-50 text-purple-600 px-2 py-1 rounded-md mb-2 inline-block">{{ item['ANO-DE-INICIO'] }} - {{ item['ANO-DE-CONCLUSAO'] || 'Atual' }}</span>
        <h4 class="text-lg font-bold">Doutorado em {{ item['NOME-CURSO'] }}</h4>
        <p class="text-slate-600 font-medium">{{ item['NOME-INSTITUICAO'] }}{{ item['SIGLA-PAIS-NACIONALIDADE'] ? ', ' + item['SIGLA-PAIS-NACIONALIDADE'] : '' }}</p>
      </div>

      <!-- Mestrado -->
      <div v-for="(item, idx) in mestrados" :key="'mes-'+idx" class="relative pl-8 border-l-2 border-slate-100 pb-2">
         <div class="absolute w-4 h-4 bg-indigo-500 border-4 border-white rounded-full -left-[9px] top-1"></div>
         <span class="text-xs font-bold bg-indigo-50 text-indigo-600 px-2 py-1 rounded-md mb-2 inline-block">{{ item['ANO-DE-INICIO'] }} - {{ item['ANO-DE-CONCLUSAO'] || 'Atual' }}</span>
         <h4 class="text-lg font-bold">Mestrado em {{ item['NOME-CURSO'] }}</h4>
         <p class="text-slate-600 font-medium">{{ item['NOME-INSTITUICAO'] }}{{ item['SIGLA-PAIS-NACIONALIDADE'] ? ', ' + item['SIGLA-PAIS-NACIONALIDADE'] : '' }}</p>
      </div>

      <!-- Graduação -->
      <div v-for="(item, idx) in graduacoes" :key="'grad-'+idx" class="relative pl-8 border-l-2 border-transparent pb-2">
        <div class="absolute w-4 h-4 bg-blue-500 border-4 border-white rounded-full -left-[9px] top-1"></div>
        <span class="text-xs font-bold bg-blue-50 text-blue-600 px-2 py-1 rounded-md mb-2 inline-block">{{ item['ANO-DE-INICIO'] }} - {{ item['ANO-DE-CONCLUSAO'] || 'Atual' }}</span>
        <h4 class="text-lg font-bold">Graduação em {{ item['NOME-CURSO'] }}</h4>
        <p class="text-slate-600 font-medium">{{ item['NOME-INSTITUICAO'] }}</p>
      </div>
    </div>

    <!-- Separador e seção de Pós-Doutorado -->
    <div v-if="posDoutorados.length" class="mt-12">
      <div class="relative py-4">
        <div class="absolute inset-0 flex items-center" aria-hidden="true">
          <div class="w-full border-t border-slate-200"></div>
        </div>
        <div class="relative flex justify-center">
          <span class="bg-white px-4 text-xs font-black text-slate-400 uppercase tracking-[0.2em]">Pós-Doutorado e Livre Docência</span>
        </div>
      </div>


      <div class="space-y-6 ml-2">
        <div v-for="(item, idx) in posDoutorados" :key="'pos-'+idx" class="relative pl-8 border-l-2 border-slate-100 pb-2">
          <div class="absolute w-4 h-4 bg-fuchsia-500 border-4 border-white rounded-full -left-[9px] top-1"></div>
          <span class="text-xs font-bold bg-fuchsia-50 text-fuchsia-600 px-2 py-1 rounded-md mb-2 inline-block">{{ item['ANO-DE-INICIO'] }} - {{ item['ANO-DE-CONCLUSAO'] || 'Atual' }}</span>
          <h4 class="text-lg font-bold">Pós-Doutorado</h4>
          <p class="text-slate-600 font-medium">{{ item['NOME-INSTITUICAO'] }}</p>
        </div>
      </div>
    </div>

  </div>
</template>