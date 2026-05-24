import { ref } from 'vue'
import api from '../api/axios'
import { BRANCHES as DEFAULT_BRANCHES } from '../constants/branches'

export function useBranches() {
  const branches = ref([...DEFAULT_BRANCHES])

  async function loadBranches() {
    try {
      const res = await api.get('/branches/')
      const names = (res.data || []).map(item => item.name).filter(Boolean)
      branches.value = names.length ? names : [...DEFAULT_BRANCHES]
    } catch {
      branches.value = [...DEFAULT_BRANCHES]
    }
  }

  async function addBranch(name) {
    const cleanName = String(name || '').trim()
    if (!cleanName) throw new Error('Filial nomini kiriting.')

    const res = await api.post('/branches/', { name: cleanName })
    const savedName = res.data?.name || cleanName
    if (!branches.value.some(branch => branch.toLowerCase() === savedName.toLowerCase())) {
      branches.value.push(savedName)
      branches.value.sort((a, b) => a.localeCompare(b))
    }
    return savedName
  }

  return { branches, loadBranches, addBranch }
}
