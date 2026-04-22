<script setup>
import { computed } from 'vue'
import { GraduationCap, Users, ExternalLink } from 'lucide-vue-next'

const props = defineProps({
  orientacoes: Object
})

const getOrientadoInfo = (item, tagBase) => {
  const db = item[`DADOS-BASICOS-DE-${tagBase}`] || {}
  const det = item[`DETALHAMENTO-DE-${tagBase}`] || {}
  return {
    titulo: db['TITULO'] || db['TITULO-DO-TRABALHO'] || '',
    ano: db['ANO'] || '',
    tipo: db['TIPO-DE-ORIENTACAO'] || '',
    nomeOrientado: det['NOME-DO-ORIENTADO'] || det['NOME-DO-ORIENTANDO'] || '',
    idLattes: det['NRO-ID-CNPQ'] || det['NUMERO-ID-ORIENTADO'] || '',
  }
}

const getOrientadoInfoIC = (item) => {
  const db = item['DADOS-BASICOS-DE-OUTRAS-ORIENTACOES-CONCLUIDAS'] || item['DADOS-BASICOS-DE-ORIENTACOES-CONCLUIDAS'] || {}
  const det = item['DETALHAMENTO-DE-OUTRAS-ORIENTACOES-CONCLUIDAS'] || item['DETALHAMENTO-DE-ORIENTACOES-CONCLUIDAS'] || {}
  return {
    titulo: db['TITULO'] || '',
    ano: db['ANO'] || '',
    nomeOrientado: det['NOME-DO-ORIENTADO'] || det['NOME-DO-ORIENTANDO'] || '',
    idLattes: det['NRO-ID-CNPQ'] || det['NUMERO-ID-ORIENTADO'] || '',
  }
}

const getAndamentoInfo = (item, tagBase) => {
  const db = item[`DADOS-BASICOS-DE-${tagBase}`] || {}
  const det = item[`DETALHAMENTO-DE-${tagBase}`] || {}
  return {
    titulo: db['TITULO-DO-TRABALHO'] || db['TITULO'] || '',
    ano: db['ANO'] || db['ANO-DE-INICIO'] || '',
    nomeOrientado: det['NOME-DO-ORIENTANDO'] || det['NOME-DO-ORIENTADO'] || '',
    idLattes: det['NRO-ID-CNPQ'] || det['NUMERO-ID-ORIENTADO'] || '',
  }
}

// Ordena uma lista de orientações por ano (mais recente primeiro)
const sortByAno = (lista, getAnoFn) => {
  return [...lista].sort((a, b) => {
    const anoA = parseInt(getAnoFn(a)) || 0
    const anoB = parseInt(getAnoFn(b)) || 0
    return anoB - anoA
  })
}

const doutoradoConcluidoSorted = computed(() =>
  sortByAno(props.orientacoes.doutoradoConcluido, item => getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO').ano)
)
const posDocConcluidoSorted = computed(() =>
  sortByAno(props.orientacoes.posDocConcluido, item => getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO').ano)
)
const mestradoConcluidoSorted = computed(() =>
  sortByAno(props.orientacoes.mestradoConcluido, item => getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-MESTRADO').ano)
)
const icConcluidaSorted = computed(() =>
  sortByAno(props.orientacoes.icConcluida, item => getOrientadoInfoIC(item).ano)
)

// Em andamento
const doutoradoAndamentoSorted = computed(() =>
  sortByAno(props.orientacoes.doutoradoAndamento, item => getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO').ano)
)
const mestradoAndamentoSorted = computed(() =>
  sortByAno(props.orientacoes.mestradoAndamento, item => getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO').ano)
)
const posDocAndamentoSorted = computed(() =>
  sortByAno(props.orientacoes.posDocAndamento, item => getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO').ano)
)
const icAndamentoSorted = computed(() =>
  sortByAno(props.orientacoes.icAndamento, item => getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA').ano)
)
</script>

<template>
  <div class="space-y-10 animate-in">
    
    <!-- Doutorado -->
    <section v-if="orientacoes.doutoradoConcluido.length || orientacoes.doutoradoAndamento.length">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-bold flex items-center gap-2"><GraduationCap class="text-purple-500" :size="20"/> Teses de Doutorado</h3>
        <div class="flex gap-2">
          <span v-if="orientacoes.doutoradoConcluido.length" class="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-xs font-bold">{{ orientacoes.doutoradoConcluido.length }} concluídas</span>
          <span v-if="orientacoes.doutoradoAndamento.length" class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-bold">{{ orientacoes.doutoradoAndamento.length }} em andamento</span>
        </div>
      </div>
      <div class="space-y-3 max-h-[500px] overflow-y-auto pr-2 scrollbar-thin">
        <!-- Concluídas -->
        <div v-for="(item, idx) in doutoradoConcluidoSorted" :key="'doc-c-'+idx" class="group bg-white border border-slate-200 hover:border-purple-300 transition-colors rounded-xl p-4 shadow-sm text-sm">
          <div class="flex items-start justify-between gap-3">
            <div class="flex-1 min-w-0">
              <h4 class="font-bold text-slate-800 leading-snug mb-1.5 group-hover:text-purple-700 transition-colors">{{ getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO').titulo || 'Sem título' }}</h4>
              <div class="flex flex-wrap items-center gap-2 text-slate-600">
                <a v-if="getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO').idLattes" :href="`https://lattes.cnpq.br/${getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO').idLattes}`" target="_blank" rel="noopener noreferrer" class="font-medium text-blue-600 hover:text-blue-800 transition-colors flex items-center gap-1">
                  {{ getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO').nomeOrientado }}
                  <ExternalLink :size="12" />
                </a>
                <span v-else class="font-medium">{{ getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO').nomeOrientado || 'Não informado' }}</span>
                <span class="font-bold text-slate-300">•</span>
                <span class="bg-purple-50 text-purple-600 px-2 py-0.5 rounded font-bold text-xs">{{ getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO').ano }}</span>
              </div>
            </div>
          </div>
        </div>
        <!-- Em andamento -->
        <div v-for="(item, idx) in doutoradoAndamentoSorted" :key="'doc-a-'+idx" class="group bg-slate-50/50 border border-dashed border-slate-200 hover:border-blue-300 transition-colors rounded-xl p-4 shadow-sm text-sm">
          <div class="flex items-start justify-between gap-3">
            <div class="flex-1 min-w-0">
              <h4 class="font-bold text-slate-700 leading-snug mb-1.5">{{ getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO').titulo || 'Sem título' }}</h4>
              <div class="flex flex-wrap items-center gap-2 text-slate-500 italic">
                <span>{{ getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO').nomeOrientado }}</span>
                <span class="font-bold text-slate-300">•</span>
                <span class="text-xs bg-blue-50 text-blue-600 px-2 py-0.5 rounded not-italic font-bold">Desde {{ getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-DOUTORADO').ano }}</span>
                <span class="text-xs text-blue-500 font-bold not-italic font-mono ml-auto">EM ANDAMENTO</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Mestrado -->
    <section v-if="orientacoes.mestradoConcluido.length || orientacoes.mestradoAndamento.length">
      <div class="flex items-center justify-between mb-4 border-t pt-6">
        <h3 class="text-lg font-bold flex items-center gap-2"><GraduationCap class="text-indigo-500" :size="20"/> Dissertações de Mestrado</h3>
        <div class="flex gap-2">
          <span v-if="orientacoes.mestradoConcluido.length" class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-xs font-bold">{{ orientacoes.mestradoConcluido.length }} concluídas</span>
          <span v-if="orientacoes.mestradoAndamento.length" class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-bold">{{ orientacoes.mestradoAndamento.length }} em andamento</span>
        </div>
      </div>
      <div class="space-y-3 max-h-[500px] overflow-y-auto pr-2 scrollbar-thin">
        <!-- Concluídas -->
        <div v-for="(item, idx) in mestradoConcluidoSorted" :key="'mes-c-'+idx" class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm text-sm">
          <h4 class="font-bold text-slate-800 mb-1.5">{{ getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-MESTRADO').titulo || 'Sem título' }}</h4>
          <div class="flex flex-wrap items-center gap-2 text-slate-600">
            <a v-if="getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-MESTRADO').idLattes" :href="`https://lattes.cnpq.br/${getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-MESTRADO').idLattes}`" target="_blank" rel="noopener noreferrer" class="font-medium text-blue-600 hover:text-blue-800 transition-colors flex items-center gap-1">
              {{ getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-MESTRADO').nomeOrientado }}
              <ExternalLink :size="12" />
            </a>
            <span v-else class="font-medium">{{ getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-MESTRADO').nomeOrientado }}</span>
            <span class="font-bold text-slate-300">•</span>
            <span class="bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded font-bold text-xs">{{ getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-MESTRADO').ano }}</span>
          </div>
        </div>
        <!-- Em andamento -->
        <div v-for="(item, idx) in mestradoAndamentoSorted" :key="'mes-a-'+idx" class="bg-slate-50/50 border border-dashed border-slate-200 rounded-xl p-4 shadow-sm text-sm">
          <h4 class="font-bold text-slate-700 mb-1.5">{{ getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO').titulo || 'Sem título' }}</h4>
          <div class="flex items-center gap-2 text-slate-500 italic">
            <span>{{ getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO').nomeOrientado }}</span>
            <span class="font-bold text-slate-300">•</span>
            <span class="text-xs bg-blue-50 text-blue-600 px-2 py-0.5 rounded not-italic font-bold">Desde {{ getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-MESTRADO').ano }}</span>
            <span class="text-xs text-blue-500 font-bold not-italic font-mono ml-auto">EM ANDAMENTO</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Iniciação Científica -->
    <section v-if="orientacoes.icConcluida.length || orientacoes.icAndamento.length">
      <div class="flex items-center justify-between mb-4 border-t pt-6">
        <h3 class="text-lg font-bold flex items-center gap-2"><Users class="text-blue-500" :size="20"/> Iniciação Científica</h3>
        <div class="flex gap-2">
          <span v-if="orientacoes.icConcluida.length" class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-bold">{{ orientacoes.icConcluida.length }} concluídas</span>
          <span v-if="orientacoes.icAndamento.length" class="bg-cyan-100 text-cyan-700 px-3 py-1 rounded-full text-xs font-bold">{{ orientacoes.icAndamento.length }} em andamento</span>
        </div>
      </div>
      <div class="space-y-3 max-h-[500px] overflow-y-auto pr-2 scrollbar-thin">
        <!-- Concluídas -->
        <div v-for="(item, idx) in icConcluidaSorted" :key="'ic-c-'+idx" class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm text-sm">
          <h4 class="font-bold text-slate-800 mb-1.5">{{ getOrientadoInfoIC(item).titulo || 'Sem título' }}</h4>
          <p class="text-slate-600 font-medium">{{ getOrientadoInfoIC(item).nomeOrientado }}
            <span class="bg-blue-50 text-blue-600 px-2 py-0.5 rounded font-bold text-xs ml-2">{{ getOrientadoInfoIC(item).ano }}</span>
          </p>
        </div>
        <!-- Em andamento -->
        <div v-for="(item, idx) in icAndamentoSorted" :key="'ic-a-'+idx" class="bg-slate-50/50 border border-dashed border-slate-200 rounded-xl p-4 shadow-sm text-sm">
          <h4 class="font-bold text-slate-700 mb-1.5">{{ getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA').titulo || 'Sem título' }}</h4>
          <div class="flex items-center gap-2 text-slate-500 italic">
            <span>{{ getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA').nomeOrientado }}</span>
            <span class="font-bold text-slate-300">•</span>
            <span class="text-xs bg-cyan-50 text-cyan-600 px-2 py-0.5 rounded not-italic font-bold">Desde {{ getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-INICIACAO-CIENTIFICA').ano }}</span>
            <span class="text-xs text-cyan-500 font-bold not-italic font-mono ml-auto">EM ANDAMENTO</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Supervisão de Pós-Doutorado -->
    <section v-if="orientacoes.posDocConcluido.length || orientacoes.posDocAndamento.length">
      <div class="flex items-center justify-between mb-4 border-t pt-6">
        <h3 class="text-lg font-bold flex items-center gap-2"><Users class="text-fuchsia-500" :size="20"/> Supervisão de Pós-Doutorado</h3>
        <div class="flex gap-2">
          <span v-if="orientacoes.posDocConcluido.length" class="bg-fuchsia-100 text-fuchsia-700 px-3 py-1 rounded-full text-xs font-bold">{{ orientacoes.posDocConcluido.length }} concluídas</span>
          <span v-if="orientacoes.posDocAndamento.length" class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-xs font-bold">{{ orientacoes.posDocAndamento.length }} em andamento</span>
        </div>
      </div>
      <div class="space-y-3 max-h-[500px] overflow-y-auto pr-2 scrollbar-thin">
        <!-- Concluídas -->
        <div v-for="(item, idx) in posDocConcluidoSorted" :key="'pd-c-'+idx" class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm text-sm">
          <h4 class="font-bold text-slate-800 mb-1.5">{{ getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO').titulo || 'Sem título' }}</h4>
          <p class="text-slate-600 font-medium">{{ getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO').nomeOrientado }} 
            <span class="bg-fuchsia-50 text-fuchsia-600 px-2 py-0.5 rounded font-bold text-xs ml-2">{{ getOrientadoInfo(item, 'ORIENTACOES-CONCLUIDAS-PARA-POS-DOUTORADO').ano }}</span>
          </p>
        </div>
        <!-- Em andamento -->
        <div v-for="(item, idx) in posDocAndamentoSorted" :key="'pd-a-'+idx" class="bg-slate-50/50 border border-dashed border-slate-200 rounded-xl p-4 shadow-sm text-sm">
          <h4 class="font-bold text-slate-700 mb-1.5">{{ getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO').titulo || 'Sem título' }}</h4>
          <div class="flex items-center gap-2 text-slate-500 italic">
            <span>{{ getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO').nomeOrientado }}</span>
            <span class="font-bold text-slate-300">•</span>
            <span class="text-xs bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded not-italic font-bold">Desde {{ getAndamentoInfo(item, 'ORIENTACAO-EM-ANDAMENTO-DE-POS-DOUTORADO').ano }}</span>
            <span class="text-xs text-indigo-500 font-bold not-italic font-mono ml-auto">EM ANDAMENTO</span>
          </div>
        </div>
      </div>
    </section>

    <div v-if="!orientacoes.doutoradoConcluido.length && !orientacoes.mestradoConcluido.length && !orientacoes.posDocConcluido.length && !orientacoes.icConcluida.length && !orientacoes.doutoradoAndamento.length && !orientacoes.mestradoAndamento.length && !orientacoes.posDocAndamento.length && !orientacoes.icAndamento.length" class="text-slate-500 italic p-6 text-center border border-dashed rounded-xl bg-slate-50">
      Nenhuma orientação registrada.
    </div>
  </div>
</template>

