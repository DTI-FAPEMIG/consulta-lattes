<script setup>
import { FileText, User, MapPin, Target } from 'lucide-vue-next'

defineProps({
  dadosGerais: Object,
  enderecoProfissional: Object,
  areasAtuacao: Array
})
</script>

<template>
  <div class="space-y-8 animate-in">
    <div v-if="dadosGerais['RESUMO-CV']">
      <h3 class="text-lg font-bold flex items-center gap-2 mb-3"><FileText class="text-blue-500" :size="20"/> Resumo</h3>
      <p class="text-slate-600 leading-relaxed text-justify bg-slate-50 p-6 rounded-2xl text-sm">{{ dadosGerais['RESUMO-CV']['TEXTO-RESUMO-CV-RH'] || 'Nenhum resumo.' }}</p>
    </div>
    <div class="grid md:grid-cols-2 gap-4">
      <div class="border border-slate-100 p-5 rounded-2xl flex gap-4">
        <div class="bg-blue-50 text-blue-500 p-3 rounded-xl h-fit"><User :size="20"/></div>
        <div>
          <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Nacionalidade</p>
          <p class="font-medium">{{ dadosGerais['NACIONALIDADE'] || '-' }} - {{ dadosGerais['PAIS-DE-NASCIMENTO'] || '-' }}</p>
        </div>
      </div>
      <div class="border border-slate-100 p-5 rounded-2xl flex gap-4">
        <div class="bg-emerald-50 text-emerald-500 p-3 rounded-xl h-fit"><MapPin :size="20"/></div>
        <div>
          <p class="text-xs font-bold text-slate-400 uppercase tracking-wider mb-1">Endereço Profissional</p>
          <p class="font-medium">{{ [enderecoProfissional['NOME-INSTITUICAO-EMPRESA'], enderecoProfissional['NOME-ORGAO']].filter(Boolean).join(', ') || 'Não informado' }}</p>
        </div>
      </div>
    </div>
    <div v-if="areasAtuacao.length">
      <h3 class="text-lg font-bold flex items-center gap-2 mb-4"><Target class="text-purple-500" :size="20"/> Áreas de Atuação</h3>
      <div class="flex flex-wrap gap-2"><span v-for="(area, idx) in areasAtuacao" :key="idx" class="bg-purple-50 text-purple-700 px-3 py-1.5 rounded-lg text-sm font-medium border border-purple-100">{{ area['NOME-DA-ESPECIALIDADE'] || area['NOME-DA-SUB-AREA-DO-CONHECIMENTO'] || area['NOME-DA-AREA-DO-CONHECIMENTO'] || area['NOME-GRANDE-AREA-DO-CONHECIMENTO'] }}</span></div>
    </div>
  </div>
</template>