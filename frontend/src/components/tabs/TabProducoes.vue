<script setup>
import { computed } from 'vue'
import { BookOpen, Calendar, Presentation, BookMarked, FileText } from 'lucide-vue-next'

const props = defineProps({
  artigos: Array,
  capitulosLivros: Array,
  trabalhosAnais: Array,
  patentes: Array
})

// Ordena por ano (campo pode variar conforme a estrutura do objeto)
const sortByAno = (lista, getAnoFn) =>
  [...lista].sort((a, b) => (parseInt(getAnoFn(b)) || 0) - (parseInt(getAnoFn(a)) || 0))

const artigosSorted = computed(() =>
  sortByAno(props.artigos, a => a['DADOS-BASICOS-DO-ARTIGO']?.['ANO-DO-ARTIGO'])
)
const capitulosSorted = computed(() =>
  sortByAno(props.capitulosLivros, c => c['DADOS-BASICOS-DO-CAPITULO']?.['ANO'])
)
const trabalhosSorted = computed(() =>
  sortByAno(props.trabalhosAnais, t => t['DADOS-BASICOS-DO-TRABALHO']?.['ANO-DO-TRABALHO'])
)
const patentesSorted = computed(() =>
  sortByAno(props.patentes, p => p['DADOS-BASICOS-DA-PATENTE']?.['ANO-DESENVOLVIMENTO'])
)
</script>

<template>
  <div class="space-y-10 animate-in">

    <!-- Artigos Publicados -->
    <section v-if="artigos.length">
      <div class="flex items-center justify-between mb-4">
        <h3 class="text-lg font-bold flex items-center gap-2"><BookOpen class="text-blue-500" :size="20"/> Artigos Publicados em Periódicos</h3>
        <span class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full text-xs font-bold">{{ artigos.length }} artigos</span>
      </div>
      <div class="space-y-4 max-h-[400px] overflow-y-auto pr-2 scrollbar-thin">
        <div v-for="(artigo, idx) in artigosSorted" :key="idx" class="group bg-white border border-slate-200 hover:border-blue-400 transition-colors rounded-xl p-4 shadow-sm text-sm">
          <h4 class="font-bold text-slate-800 leading-snug mb-2 group-hover:text-blue-700 transition-colors">{{ artigo['DADOS-BASICOS-DO-ARTIGO']?.['TITULO-DO-ARTIGO'] }}</h4>
          <div class="flex flex-wrap items-center gap-2 text-slate-600">
            <span class="bg-slate-100 px-2 py-1 rounded font-medium">{{ artigo['DETALHAMENTO-DO-ARTIGO']?.['TITULO-DO-PERIODICO-OU-REVISTA'] }}</span><span class="font-bold text-slate-300">•</span><span class="font-medium"><Calendar class="inline mr-1 -mt-0.5" :size="14"/> {{ artigo['DADOS-BASICOS-DO-ARTIGO']?.['ANO-DO-ARTIGO'] }}</span><span v-if="artigo['DADOS-BASICOS-DO-ARTIGO']?.['DOI']" class="font-bold text-slate-300">•</span><a :href="`https://doi.org/${artigo['DADOS-BASICOS-DO-ARTIGO']?.['DOI']}`" target="_blank" v-if="artigo['DADOS-BASICOS-DO-ARTIGO']?.['DOI']" class="text-blue-500 hover:text-blue-700 transition-colors">DOI</a>
          </div>
        </div>
      </div>
    </section>

    <!-- Capítulos de Livros Publicados -->
    <section v-if="capitulosLivros.length">
      <div class="flex items-center justify-between mb-4 border-t pt-6">
        <h3 class="text-lg font-bold flex items-center gap-2"><BookMarked class="text-emerald-500" :size="20"/> Capítulos de Livros Publicados</h3>
        <span class="bg-emerald-100 text-emerald-700 px-3 py-1 rounded-full text-xs font-bold">{{ capitulosLivros.length }} capítulos</span>
      </div>
      <div class="space-y-4 max-h-[400px] overflow-y-auto pr-2 scrollbar-thin">
        <div v-for="(cap, idx) in capitulosSorted" :key="idx" class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm text-sm">
          <h4 class="font-bold text-slate-800 mb-2">{{ cap['DADOS-BASICOS-DO-CAPITULO']?.['TITULO-DO-CAPITULO-DO-LIVRO'] || 'Sem título' }}</h4>
          <div class="flex flex-wrap items-center gap-2 text-slate-600">
            <span class="bg-emerald-50 px-2 py-1 rounded font-medium text-emerald-700">{{ cap['DETALHAMENTO-DO-CAPITULO']?.['TITULO-DO-LIVRO'] || '' }}</span>
            <span class="font-bold text-slate-300">•</span>
            <span class="font-medium"><Calendar class="inline mr-1 -mt-0.5" :size="14"/> {{ cap['DADOS-BASICOS-DO-CAPITULO']?.['ANO'] }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Trabalhos Completos em Anais -->
    <section v-if="trabalhosAnais.length">
      <div class="flex items-center justify-between mb-4 border-t pt-6">
        <h3 class="text-lg font-bold flex items-center gap-2"><Presentation class="text-indigo-500" :size="20"/> Trabalhos Completos em Anais de Congressos</h3>
        <span class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full text-xs font-bold">{{ trabalhosAnais.length }} trabalhos</span>
      </div>
      <div class="space-y-4 max-h-[400px] overflow-y-auto pr-2 scrollbar-thin">
        <div v-for="(evento, idx) in trabalhosSorted" :key="idx" class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm text-sm">
          <h4 class="font-bold text-slate-800 mb-2">{{ evento['DADOS-BASICOS-DO-TRABALHO']?.['TITULO-DO-TRABALHO'] }}</h4>
          <p class="text-slate-600 mb-1 italic">{{ evento['DETALHAMENTO-DO-TRABALHO']?.['NOME-DO-EVENTO'] }}</p>
          <p class="text-slate-500 font-medium text-xs">Ano: {{ evento['DADOS-BASICOS-DO-TRABALHO']?.['ANO-DO-TRABALHO'] }}</p>
        </div>
      </div>
    </section>

    <!-- Patentes e Registros -->
    <section v-if="patentes.length">
      <div class="flex items-center justify-between mb-4 border-t pt-6">
        <h3 class="text-lg font-bold flex items-center gap-2"><FileText class="text-purple-500" :size="20"/> Patentes e Registros</h3>
        <span class="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-xs font-bold">{{ patentes.length }} registros</span>
      </div>
      <div class="space-y-4 max-h-[400px] overflow-y-auto pr-2 scrollbar-thin">
        <div v-for="(patente, idx) in patentesSorted" :key="idx" class="bg-white border border-slate-200 rounded-xl p-4 shadow-sm text-sm">
          <h4 class="font-bold text-slate-800 mb-2">{{ patente['DADOS-BASICOS-DA-PATENTE']?.['TITULO'] || 'Sem título' }}</h4>
          <div class="flex flex-wrap items-center gap-2 text-slate-600">
            <span class="bg-purple-50 px-2 py-1 rounded font-medium text-purple-700">{{ patente['DADOS-BASICOS-DA-PATENTE']?.['TIPO-PATENTE'] || 'Patente' }}</span>
            <span class="font-bold text-slate-300">•</span>
            <span class="font-medium"><Calendar class="inline mr-1 -mt-0.5" :size="14"/> {{ patente['DADOS-BASICOS-DA-PATENTE']?.['ANO-DESENVOLVIMENTO'] }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- Empty state -->
    <div v-if="!artigos.length && !capitulosLivros.length && !trabalhosAnais.length && !patentes.length" class="text-slate-500 italic p-6 text-center border border-dashed rounded-xl bg-slate-50">
      Nenhuma produção registrada.
    </div>
  </div>
</template>