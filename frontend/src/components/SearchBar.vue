<script setup>
import { Search, Loader2 } from 'lucide-vue-next'

defineProps({
  modelValue: String,
  loading: Boolean
})
defineEmits(['update:modelValue', 'search'])
</script>

<template>
  <div class="relative group mb-8 max-w-2xl mx-auto">
    <div class="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
      <Search class="text-slate-400 group-focus-within:text-blue-500 transition-colors" :size="20" />
    </div>
    <input 
      :value="modelValue"
      @input="$emit('update:modelValue', $event.target.value)"
      @keyup.enter="$emit('search')"
      type="text" 
      placeholder="Digite o ID Lattes..." 
      class="block w-full pl-11 pr-36 py-4 bg-white border border-slate-200 rounded-2xl shadow-sm focus:ring-4 focus:ring-blue-100 outline-none font-medium"
    />
    <button @click="$emit('search')" :disabled="loading" class="absolute right-2 top-2 bottom-2 px-6 bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white rounded-xl font-bold transition-all flex items-center gap-2">
      <Loader2 v-if="loading" class="animate-spin" :size="18" />
      {{ loading ? 'Buscando' : 'Consultar' }}
    </button>
  </div>
</template>