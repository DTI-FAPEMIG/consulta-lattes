<script setup>
import { ref } from 'vue'
import { AlertCircle } from 'lucide-vue-next'
import { useLattes } from '../useLattes' 
import { toArray } from '../helpers'
import Login from './components/Login.vue'
import { LogOut } from 'lucide-vue-next'

const bypassAuth = false // Altere para true apenas para testes locais sem JWT
const isAuthenticated = ref(bypassAuth || !!localStorage.getItem('access_token'))

const onLoginSuccess = () => {
  isAuthenticated.value = true
}

const fazerLogout = () => {
  localStorage.removeItem('access_token')
  isAuthenticated.value = false
}

import SearchBar from './components/SearchBar.vue'
import SidebarNav from './components/SidebarNav.vue'
import ResumeHeader from './components/ResumeHeader.vue'
import TabGeral from './components/tabs/TabGeral.vue'
import TabPessoal from './components/tabs/TabPessoal.vue'
import TabFormacao from './components/tabs/TabFormacao.vue'
import TabAtuacao from './components/tabs/TabAtuacao.vue'
import TabProducoes from './components/tabs/TabProducoes.vue'
import TabOrientacoes from './components/tabs/TabOrientacoes.vue'
import TabComparativo from './components/tabs/TabComparativo.vue'

const activeTab = ref('geral')

// Estado para guardar os currículos da comparação
const curriculosComparacao = ref([])

const {
  idLattes, loading, resultado, erro, buscarCurriculo, safeData, metricas, dadosGerais, 
  enderecoProfissional, areasAtuacao, formacao, atuacoes, idiomas, premios, artigos, eventos,
  capitulosLivros, livros, trabalhosAnais, patentes, orientacoes
} = useLattes()

const onSearch = async () => {
  await buscarCurriculo()
  if (resultado.value) activeTab.value = 'geral'
}

// LÓGICA DE COMPARAÇÃO
const handleAdicionarComparacao = () => {
  if (!resultado.value) return

  // Verifica se já não adicionou esse Lattes antes
  const jaExiste = curriculosComparacao.value.some(cv => cv.idLattes === idLattes.value)
  
  if (!jaExiste) {
    // Monta um objeto resumido só com o que vai pra tabela
    const resumoCv = {
      idLattes: idLattes.value,
      nome: dadosGerais.value['NOME-COMPLETO'] || 'Nome não informado',
      ...metricas.value
    }
    
    curriculosComparacao.value.push(resumoCv)
  }
  
  // Joga o usuário direto para a tela de comparação para ele ver o resultado
  activeTab.value = 'comparativo'
}

const removerDaComparacao = (idParaRemover) => {
  curriculosComparacao.value = curriculosComparacao.value.filter(cv => cv.idLattes !== idParaRemover)
}
</script>

<template>
  <Login v-if="!isAuthenticated" @logged-in="onLoginSuccess" />

  <div v-else class="min-h-screen p-4 md:p-8 bg-slate-50/50 text-slate-800">
    <div class="max-w-6xl mx-auto">
      
      <header class="mb-12 flex flex-col items-center text-center animate-in">
        
        <h1 class="text-4xl md:text-5xl font-extrabold tracking-tight text-slate-800">
          Consulta <span class="text-blue-600">Lattes</span>
        </h1>
        <p class="text-slate-500 mt-3 font-medium text-lg">Análise e comparação de currículos</p>

        <div class="mt-8 flex items-center gap-4 opacity-90 hover:opacity-100 transition-opacity">
          <span class="text-xs font-bold text-slate-400 uppercase tracking-widest mt-1">Desenvolvido por</span>
          <div class="w-1.5 h-1.5 rounded-full bg-slate-300"></div> <img src="./assets/fapemig-logo-g.png" alt="FAPEMIG" class="h-10 md:h-12 object-contain" />
        </div>

        <button @click="fazerLogout" class="mt-8 flex items-center gap-2 text-sm font-bold text-slate-400 hover:text-red-500 transition-colors">
          <LogOut class="w-4 h-4" />
          <span>Sair do Extrator</span>
        </button>
        
      </header>

      <SearchBar v-model="idLattes" :loading="loading" @search="onSearch" />

      <div v-if="erro" class="mb-8 max-w-2xl mx-auto p-5 rounded-2xl border flex items-start gap-4 animate-in bg-red-50 border-red-200 text-red-800">
        <AlertCircle class="shrink-0" />
        <div>
          <p class="font-bold">Atenção</p>
          <p class="text-sm opacity-90">{{ erro.msg }}</p>
        </div>
      </div>

      <div v-if="resultado && !loading" class="animate-in flex flex-col lg:flex-row gap-6">
        
        <SidebarNav v-model="activeTab" />

        <div class="flex-1 min-w-0 bg-white rounded-3xl p-6 md:p-10 shadow-xl border border-slate-100">
          
          <ResumeHeader 
            :dados-gerais="dadosGerais" 
            :id-lattes="idLattes" 
            :data-atualizacao="safeData['DATA-ATUALIZACAO']"
            @adicionar-comparacao="handleAdicionarComparacao" 
          />

          <TabGeral v-if="activeTab === 'geral'" :formacao="formacao" :artigos="artigos" :eventos="eventos" :premios="premios" :metricas="metricas" :capitulos-livros="capitulosLivros" :trabalhos-anais="trabalhosAnais" :patentes="patentes" :orientacoes="orientacoes" />
          <TabPessoal v-else-if="activeTab === 'resumo'" :dados-gerais="dadosGerais" :endereco-profissional="enderecoProfissional" :areas-atuacao="areasAtuacao" />
          <TabFormacao v-else-if="activeTab === 'formacao'" :formacao="formacao" />
          <TabAtuacao v-else-if="activeTab === 'atuacao'" :atuacoes="atuacoes" />
          <TabProducoes v-else-if="activeTab === 'producoes'" :artigos="artigos" :capitulos-livros="capitulosLivros" :trabalhos-anais="trabalhosAnais" :patentes="patentes" />
          <TabOrientacoes v-else-if="activeTab === 'orientacoes'" :orientacoes="orientacoes" />

          <TabComparativo v-else-if="activeTab === 'comparativo'" :lista-curriculos="curriculosComparacao" @remover="removerDaComparacao" />

        </div>
      </div>
    </div>
  </div>
</template>

<style>
.animate-in {
  animation: slideUp 0.4s ease-out forwards;
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}

.scrollbar-hide::-webkit-scrollbar { display: none; }
.scrollbar-hide { -ms-overflow-style: none; scrollbar-width: none; }

.scrollbar-thin::-webkit-scrollbar { width: 6px; }
.scrollbar-thin::-webkit-scrollbar-track { background: transparent; }
.scrollbar-thin::-webkit-scrollbar-thumb { background-color: #cbd5e1; border-radius: 10px; }
</style>