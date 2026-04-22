<script setup>
import { ref } from 'vue'
import axios from 'axios'
import { Lock, User, AlertCircle, Loader2, Eye, EyeOff } from 'lucide-vue-next'

const emit = defineEmits(['logged-in'])

const usuario = ref('')
const senha = ref('')
const mostrarSenha = ref(false)
const loading = ref(false)
const erro = ref(null)

const fazerLogin = async () => {
  if (!usuario.value || !senha.value) return

  loading.value = true
  erro.value = null

  try {
    const resposta = await axios.post('https://api-pr-2166.plataformaevandomirra.fapemig.br/api/login', {
      login: usuario.value,
      senha: senha.value
    }, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
      }
    })

    const token = resposta.data.token || resposta.data.access_token

    if (token) {
      localStorage.setItem('access_token', token)
      emit('logged-in')
    } else {
      erro.value = "Acesso negado: Credenciais inválidas."
    }
  } catch (err) {
    if (err.response && err.response.status === 401) {
      erro.value = "Usuário ou senha incorretos."
    } else {
      erro.value = "Falha de conexão com a Plataforma FAPEMIG."
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center p-4 bg-slate-50/50">
    <div class="w-full max-w-md bg-white rounded-3xl p-8 md:p-10 shadow-xl border border-slate-100 animate-in">
      
      <div class="text-center mb-8">
        <h1 class="text-3xl font-extrabold tracking-tight text-slate-800 mb-2">
          Consulta <span class="text-blue-600">Lattes</span>
        </h1>
        <p class="text-slate-500 font-medium">Acesso Restrito FAPEMIG</p>
      </div>

      <div v-if="erro" class="mb-6 p-4 rounded-xl border flex items-start gap-3 bg-red-50 border-red-200 text-red-800 animate-in">
        <AlertCircle class="shrink-0 w-5 h-5 mt-0.5" />
        <p class="text-sm font-medium">{{ erro }}</p>
      </div>

      <form @submit.prevent="fazerLogin" class="space-y-5">
        <div class="space-y-1.5">
          <label class="text-sm font-semibold text-slate-700 ml-1">Usuário / Login</label>
          <div class="relative">
            <User class="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input 
              v-model="usuario" 
              type="text" 
              required
              class="w-full pl-11 pr-4 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              placeholder="Digite seu login corporativo"
            >
          </div>
        </div>

        <div class="space-y-1.5">
          <label class="text-sm font-semibold text-slate-700 ml-1">Senha</label>
          <div class="relative">
            <Lock class="absolute left-3.5 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input 
              v-model="senha" 
              :type="mostrarSenha ? 'text' : 'password'" 
              required
              class="w-full pl-11 pr-12 py-3 bg-slate-50 border border-slate-200 rounded-xl focus:bg-white focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none transition-all"
              placeholder="••••••••"
            >
            <button 
              type="button"
              @click="mostrarSenha = !mostrarSenha"
              class="absolute right-3.5 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 focus:outline-none transition-colors"
              title="Mostrar/Ocultar Senha"
            >
              <EyeOff v-if="!mostrarSenha" class="w-5 h-5" />
              <Eye v-else class="w-5 h-5 text-blue-600" />
            </button>
          </div>
        </div>

        <button 
          type="submit" 
          :disabled="loading"
          class="w-full flex items-center justify-center gap-2 py-3.5 mt-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl transition-colors disabled:opacity-70 disabled:cursor-not-allowed"
        >
          <Loader2 v-if="loading" class="w-5 h-5 animate-spin" />
          <span>{{ loading ? 'Autenticando...' : 'Entrar no Sistema' }}</span>
        </button>
      </form>

    </div>
  </div>
</template>

<style scoped>
.animate-in {
  animation: slideUp 0.4s ease-out forwards;
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(15px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
