<script setup>
import { computed } from 'vue'
import { GraduationCap, BookOpen, Presentation, Medal, Award, BookMarked, FileText, ShieldCheck } from 'lucide-vue-next'
import { toArray } from '../../../helpers'

const props = defineProps({
  formacao: Object,
  artigos: Array,
  eventos: Array,
  premios: Array,
  metricas: Object,
  capitulosLivros: Array,
  trabalhosAnais: Array,
  patentes: Array,
  orientacoes: Object
})

const quantitativos = computed(() => ({
  graduacoes: toArray(props.formacao['GRADUACAO']).length,
  especializacoes: toArray(props.formacao['ESPECIALIZACAO']).length,
  mestrados: toArray(props.formacao['MESTRADO']).length,
  doutorados: toArray(props.formacao['DOUTORADO']).length,
  posDoutorados: toArray(props.formacao['POS-DOUTORADO']).length,
  artigos: props.artigos.length,
  trabalhosAnais: props.trabalhosAnais.length,
  capitulosLivros: props.capitulosLivros.length,
  patentes: props.patentes.length,
  premios: props.premios.length,
  orientacoesDoutorado: (props.orientacoes?.doutoradoConcluido?.length || 0) + (props.orientacoes?.doutoradoAndamento?.length || 0),
  orientacoesMestrado: (props.orientacoes?.mestradoConcluido?.length || 0) + (props.orientacoes?.mestradoAndamento?.length || 0),
  orientacoesIC: (props.orientacoes?.icConcluida?.length || 0) + (props.orientacoes?.icAndamento?.length || 0),
}))

const nivelBolsaPQ = computed(() => props.metricas?.nivel_atual_bolsa_pq || null)
</script>

<template>
  <div class="space-y-8 animate-in">

    <!-- Badge Bolsa PQ -->
    <div v-if="nivelBolsaPQ && nivelBolsaPQ !== 'Não identificada'" class="flex items-center gap-3 bg-gradient-to-r from-amber-50 to-yellow-50 border border-amber-200 rounded-2xl p-4">
      <div class="bg-amber-100 text-amber-600 p-2.5 rounded-xl">
        <ShieldCheck :size="22" />
      </div>
      <div>
        <p class="font-black text-amber-800 text-sm">Bolsista de Produtividade em Pesquisa do CNPq</p>
        <p class="text-amber-600 text-xs font-bold mt-0.5">Nível {{ nivelBolsaPQ }}</p>
      </div>
    </div>

    <div>
      <h3 class="text-lg font-bold flex items-center gap-2 mb-4"><GraduationCap class="text-blue-500" :size="20"/> Quantitativo Acadêmico</h3>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-5 gap-4">
        <div class="p-6 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all"><p class="text-3xl font-black text-slate-800">{{ quantitativos.graduacoes }}</p><p class="text-slate-500 text-sm font-semibold uppercase tracking-wide mt-1">Graduação</p></div>
        <div class="p-6 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all"><p class="text-3xl font-black text-slate-800">{{ quantitativos.especializacoes }}</p><p class="text-slate-500 text-sm font-semibold uppercase tracking-wide mt-1">Espec.</p></div>
        <div class="p-6 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all"><p class="text-3xl font-black text-slate-800">{{ quantitativos.mestrados }}</p><p class="text-slate-500 text-sm font-semibold uppercase tracking-wide mt-1">Mestrado</p></div>
        <div class="p-6 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all"><p class="text-3xl font-black text-slate-800">{{ quantitativos.doutorados }}</p><p class="text-slate-500 text-sm font-semibold uppercase tracking-wide mt-1">Doutorado</p></div>
        <div class="p-6 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all"><p class="text-3xl font-black text-slate-800">{{ quantitativos.posDoutorados }}</p><p class="text-slate-500 text-sm font-semibold uppercase tracking-wide mt-1">Pós-Dout.</p></div>
      </div>
    </div>

    <div>
      <h3 class="text-lg font-bold flex items-center gap-2 mb-4 mt-8"><BookOpen class="text-indigo-500" :size="20"/> Produções e Reconhecimento</h3>
      <div class="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all flex items-center gap-4">
          <div class="bg-indigo-100 p-3 rounded-xl text-indigo-600"><BookOpen :size="22"/></div>
          <div><p class="text-2xl font-black text-slate-800">{{ quantitativos.artigos }}</p><p class="text-slate-500 text-xs font-bold uppercase tracking-wide">Artigos</p></div>
        </div>
        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all flex items-center gap-4">
          <div class="bg-blue-100 p-3 rounded-xl text-blue-600"><Presentation :size="22"/></div>
          <div><p class="text-2xl font-black text-slate-800">{{ quantitativos.trabalhosAnais }}</p><p class="text-slate-500 text-xs font-bold uppercase tracking-wide">Trab. Anais</p></div>
        </div>
        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all flex items-center gap-4">
          <div class="bg-emerald-100 p-3 rounded-xl text-emerald-600"><BookMarked :size="22"/></div>
          <div><p class="text-2xl font-black text-slate-800">{{ quantitativos.capitulosLivros }}</p><p class="text-slate-500 text-xs font-bold uppercase tracking-wide">Cap. Livros</p></div>
        </div>
        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all flex items-center gap-4">
          <div class="bg-purple-100 p-3 rounded-xl text-purple-600"><FileText :size="22"/></div>
          <div><p class="text-2xl font-black text-slate-800">{{ quantitativos.patentes }}</p><p class="text-slate-500 text-xs font-bold uppercase tracking-wide">Patentes</p></div>
        </div>
        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all flex items-center gap-4">
          <div class="bg-amber-100 p-3 rounded-xl text-amber-600"><Medal :size="22"/></div>
          <div><p class="text-2xl font-black text-slate-800">{{ quantitativos.premios }}</p><p class="text-slate-500 text-xs font-bold uppercase tracking-wide">Prêmios</p></div>
        </div>
      </div>
    </div>

    <div>
      <h3 class="text-lg font-bold flex items-center gap-2 mb-4 mt-8"><GraduationCap class="text-purple-500" :size="20"/> Orientações</h3>
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all flex items-center gap-4">
          <div class="bg-purple-100 p-3 rounded-xl text-purple-600"><GraduationCap :size="22"/></div>
          <div><p class="text-2xl font-black text-slate-800">{{ quantitativos.orientacoesDoutorado }}</p><p class="text-slate-500 text-xs font-bold uppercase tracking-wide">Doutorado</p></div>
        </div>
        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all flex items-center gap-4">
          <div class="bg-indigo-100 p-3 rounded-xl text-indigo-600"><GraduationCap :size="22"/></div>
          <div><p class="text-2xl font-black text-slate-800">{{ quantitativos.orientacoesMestrado }}</p><p class="text-slate-500 text-xs font-bold uppercase tracking-wide">Mestrado</p></div>
        </div>
        <div class="p-5 rounded-2xl bg-slate-50 border border-slate-100 hover:bg-white hover:shadow-md transition-all flex items-center gap-4">
          <div class="bg-blue-100 p-3 rounded-xl text-blue-600"><GraduationCap :size="22"/></div>
          <div><p class="text-2xl font-black text-slate-800">{{ quantitativos.orientacoesIC }}</p><p class="text-slate-500 text-xs font-bold uppercase tracking-wide">Init. Cient.</p></div>
        </div>
      </div>
    </div>

    <!-- Prêmios e Títulos -->
    <div v-if="premios.length">
      <h3 class="text-lg font-bold flex items-center gap-2 mb-4 mt-8"><Award class="text-amber-500" :size="20"/> Prêmios e Títulos</h3>
      <div class="grid gap-3">
        <div v-for="(premio, idx) in premios" :key="idx" class="flex gap-3 items-center bg-white border border-amber-200 p-4 rounded-xl shadow-sm">
          <div class="bg-amber-100 p-2.5 rounded-full text-amber-600 shrink-0"><Medal :size="18"/></div>
          <div>
            <p class="font-bold text-slate-800 text-sm">{{ premio['NOME-DO-PREMIO-OU-TITULO'] }}</p>
            <p class="text-xs text-slate-500 font-medium mt-0.5">{{ premio['NOME-DA-ENTIDADE-PROMOTORA'] }} <span class="text-amber-600 ml-1">({{ premio['ANO-DA-PREMIACAO'] }})</span></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>