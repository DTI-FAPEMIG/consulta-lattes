<script setup>
import { Calendar, PlusCircle } from 'lucide-vue-next'
import { formatarData } from '../../helpers'

defineProps({
  dadosGerais: Object,
  idLattes: String,
  dataAtualizacao: String
})

// Precisamos emitir um evento para avisar o App.vue que o botão foi clicado
defineEmits(['adicionar-comparacao'])
</script>

<template>
  <div class="mb-8 pb-6 border-b border-slate-100 flex flex-col md:flex-row md:items-start justify-between gap-4">
    <div>
      <h2 class="text-3xl font-black capitalize">{{ dadosGerais['NOME-COMPLETO'] || 'Nome não informado' }}</h2>
      <p class="text-slate-500 mt-1 font-medium">Nome em Citações: {{ dadosGerais['NOME-EM-CITACOES-BIBLIOGRAFICAS'] || '-' }}</p>
      
      <button 
        @click="$emit('adicionar-comparacao')"
        class="mt-4 flex items-center gap-2 bg-indigo-50 hover:bg-indigo-100 text-indigo-700 px-4 py-2 rounded-xl font-bold text-sm transition-colors border border-indigo-200"
      >
        <PlusCircle :size="16" /> Adicionar à Comparação
      </button>
    </div>

    <div class="flex flex-col items-end gap-2 mt-2 md:mt-0">
      <span class="text-xs bg-slate-50 px-3 py-1.5 rounded-lg font-bold border flex items-center gap-1.5 text-slate-500">
        <Calendar :size="14"/> Atualizado: {{ formatarData(dataAtualizacao) }}
      </span>
      <span class="text-xs text-slate-400 font-mono">Lattes: {{ idLattes }}</span>
    </div>
  </div>
</template>