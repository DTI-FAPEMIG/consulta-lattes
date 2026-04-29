<script setup>
import { Award, Medal, Globe } from 'lucide-vue-next'

defineProps({
  premios: Array,
  idiomas: Array
})
</script>

<template>
  <div class="space-y-10 animate-in">
    <div>
      <h3 class="text-lg font-bold flex items-center gap-2 mb-4"><Award class="text-amber-500" :size="20"/> Prêmios e Títulos</h3>
      <div class="grid gap-3">
        <div v-for="(premio, idx) in premios" :key="idx" class="flex gap-4 items-center bg-white border border-amber-200 p-4 rounded-xl shadow-sm"><div class="bg-amber-100 p-3 rounded-full text-amber-600 shrink-0"><Medal :size="20"/></div><div><p class="font-bold text-slate-800 text-sm md:text-base">{{ premio['NOME-DO-PREMIO-OU-TITULO'] }}</p><p class="text-xs md:text-sm text-slate-500 font-medium mt-1">{{ premio['NOME-DA-ENTIDADE-PROMOTORA'] }} <span class="text-amber-600 ml-1">({{ premio['ANO-DA-PREMIACAO'] }})</span></p></div></div>
      </div>
      <p v-if="!premios.length" class="text-slate-500 italic">Nenhum prêmio registrado.</p>
    </div>
    <div>
      <h3 class="text-lg font-bold flex items-center gap-2 mb-4"><Globe class="text-emerald-500" :size="20"/> Idiomas</h3>
      <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-4">
        <div v-for="(idioma, idx) in idiomas" :key="idx" class="bg-white border border-emerald-200 p-5 rounded-2xl shadow-sm">
          <p class="text-lg font-black text-emerald-800 mb-3 border-b border-emerald-100 pb-2">{{ idioma['DESCRICAO-DO-IDIOMA'] || idioma['IDIOMA'] }}</p>
          <div class="text-sm space-y-2 text-slate-600"><div class="flex justify-between"><span>Compreensão:</span> <span class="font-bold text-slate-800">{{ idioma['PROFICIENCIA-DE-COMPREENSAO'] }}</span></div><div class="flex justify-between"><span>Leitura:</span> <span class="font-bold text-slate-800">{{ idioma['PROFICIENCIA-DE-LEITURA'] }}</span></div><div class="flex justify-between"><span>Fala:</span> <span class="font-bold text-slate-800">{{ idioma['PROFICIENCIA-DE-FALA'] }}</span></div><div class="flex justify-between"><span>Escrita:</span> <span class="font-bold text-slate-800">{{ idioma['PROFICIENCIA-DE-ESCRITA'] }}</span></div></div>
        </div>
      </div>
      <p v-if="!idiomas.length" class="text-slate-500 italic">Nenhum idioma registrado.</p>
    </div>
  </div>
</template>