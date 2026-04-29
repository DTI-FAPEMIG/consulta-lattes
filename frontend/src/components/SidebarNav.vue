<script setup>
import { LayoutDashboard, User, GraduationCap, Briefcase, BookOpen, Users, GitCompare } from 'lucide-vue-next'

defineProps({
  modelValue: String
})
defineEmits(['update:modelValue'])

const tabs = [
  { id: 'geral', icon: LayoutDashboard, label: 'Visão Geral' },
  { id: 'resumo', icon: User, label: 'Pessoal' },
  { id: 'formacao', icon: GraduationCap, label: 'Formação' },
  { id: 'atuacao', icon: Briefcase, label: 'Profissional' },
  { id: 'producoes', icon: BookOpen, label: 'Produções' },
  { id: 'orientacoes', icon: Users, label: 'Orientações' },
  { id: 'comparativo', icon: GitCompare, label: 'Comparar' }
]
</script>

<template>
  <div class="w-full lg:w-64 shrink-0 flex lg:flex-col gap-2 overflow-x-auto pb-2 lg:pb-0 scrollbar-hide">
    <button 
      v-for="tab in tabs" :key="tab.id"
      @click="$emit('update:modelValue', tab.id)" 
      :class="modelValue === tab.id ? 'bg-blue-600 text-white shadow-md' : 'bg-white text-slate-600 hover:bg-slate-100'" 
      class="px-5 py-4 rounded-2xl font-bold text-left flex items-center gap-3 transition-all whitespace-nowrap"
    ><component :is="tab.icon" :size="20" /> {{ tab.label }}</button>
  </div>
</template>