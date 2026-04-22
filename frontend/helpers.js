// Garante que o retorno seja sempre um array iterável (evita erros em v-for)
export const toArray = (item) => {
  if (!item) return []
  return Array.isArray(item) ? item : [item]
}

export const formatarData = (dataString) => {
  if (!dataString) return 'Sem data'

  // Garante que estamos lidando com uma string
  const str = String(dataString).trim()

  // Verifica se é o padrão Lattes de 8 dígitos juntos (ex: "06042026")
  if (str.length === 8 && !str.includes('/') && !str.includes('-')) {
    return `${str.substring(0, 2)}/${str.substring(2, 4)}/${str.substring(4, 8)}`
  }

  // Fallback
  let data = new Date(str)
  if (str.includes('/')) {
    const [dia, mes, ano] = str.split('/')
    data = new Date(ano, mes - 1, dia)
  }

  return isNaN(data.getTime()) ? 'Data inválida' : new Intl.DateTimeFormat('pt-BR').format(data)
}