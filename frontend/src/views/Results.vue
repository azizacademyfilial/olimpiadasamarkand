<template>
  <div>
    <div class="page-head">
      <div>
        <h2>Natijalar</h2>
        <p>Test va mental arifmetika natijalari: o‘quvchi, fan, daraja, nechtadan nechta to‘g‘ri va foiz</p>
      </div>
      <button class="primary-btn" @click="downloadExcel">Natijalarni Excelga yuklash</button>
    </div>

    <div class="filter-bar">
      <select v-if="mainAdmin" v-model="filters.center" @change="loadResults">
        <option value="">Barchasi</option>
        <option v-for="center in centers" :key="center.id" :value="center.id">{{ center.name }}</option>
      </select>
      <select v-model="filters.branch" :disabled="!mainAdmin" @change="loadResults">
        <option value="">Barcha filiallar</option>
        <option v-for="branch in branches" :key="branch" :value="branch">{{ branch }}</option>
      </select>
      <button class="secondary-btn" @click="loadResults">Yangilash</button>
    </div>

    <div v-if="mainAdmin" class="filter-bar">
      <input v-model="newBranchName" placeholder="Yangi filial nomi" />
      <button class="secondary-btn" :disabled="addingBranch" @click="createBranch">
        {{ addingBranch ? 'Qo‘shilmoqda...' : '+ Filial qo‘shish' }}
      </button>
      <span v-if="branchMessage" class="success-text">{{ branchMessage }}</span>
      <span v-if="branchError" class="error-text">{{ branchError }}</span>
    </div>

    <div class="panel">
      <div class="table-wrap">
        <table>
          <thead>
            <tr>
              <th>№</th>
              <th>O‘quvchi</th>
              <th>Fan</th>
              <th>Daraja</th>
              <th>O‘quv markaz</th>
              <th>Filial</th>
              <th>Code</th>
              <th>Nechta to‘g‘ri</th>
              <th>Foiz</th>
              <th>Vaqt</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(r, i) in results" :key="r.id">
              <td>{{ i + 1 }}</td>
              <td><b>{{ r.student_full_name }}</b></td>
              <td>{{ r.subject_name }}</td>
              <td>{{ r.level_name }}</td>
              <td>{{ r.center_name }}</td>
              <td>{{ r.student_branch }}</td>
              <td>{{ r.student_code }}</td>
              <td><b>{{ r.correct_count }}/{{ r.total_questions }}</b></td>
              <td>{{ r.percent }}%</td>
              <td>{{ formatSeconds(r.spent_seconds) }}</td>
            </tr>
            <tr v-if="!results.length">
              <td colspan="10" class="empty-cell">Natija topilmadi</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import api from '../api/axios'
import { useBranches } from '../composables/useBranches'
import { useCenters } from '../composables/useCenters'
import { fetchCurrentAdmin, getStoredAdminProfile, isMainAdmin } from '../utils/auth'

const results = ref([])
const currentAdmin = ref(getStoredAdminProfile())
const { branches, loadBranches, addBranch } = useBranches()
const { centers, loadCenters } = useCenters()
const newBranchName = ref('')
const addingBranch = ref(false)
const branchMessage = ref('')
const branchError = ref('')
const filters = reactive({ center: '', branch: '' })
const mainAdmin = computed(() => isMainAdmin(currentAdmin.value))

function formatSeconds(seconds) {
  const total = Number(seconds || 0)
  const min = Math.floor(total / 60)
  const sec = total % 60
  return `${min} daq ${sec} sek`
}

async function createBranch() {
  branchMessage.value = ''
  branchError.value = ''
  addingBranch.value = true
  try {
    const savedName = await addBranch(newBranchName.value)
    filters.branch = savedName
    newBranchName.value = ''
    branchMessage.value = 'Filial qo‘shildi.'
    await Promise.all([loadBranches(), loadCenters()])
    await loadResults()
  } catch (e) {
    branchError.value = e.message || JSON.stringify(e.response?.data || 'Filial qo‘shishda xatolik')
  } finally {
    addingBranch.value = false
  }
}

async function loadCurrentAdmin() {
  try {
    currentAdmin.value = await fetchCurrentAdmin()
    if (!mainAdmin.value && currentAdmin.value?.branch) filters.branch = currentAdmin.value.branch
  } catch {
    currentAdmin.value = getStoredAdminProfile()
  }
}

async function loadResults() {
  const params = {}
  if (filters.center && mainAdmin.value) params.center = filters.center
  if (filters.branch && mainAdmin.value) params.branch = filters.branch
  const res = await api.get('/results/', { params })
  results.value = res.data
}

async function downloadExcel() {
  const params = {}
  if (filters.center && mainAdmin.value) params.center = filters.center
  if (filters.branch && mainAdmin.value) params.branch = filters.branch
  const res = await api.get('/results/export-excel/', { params, responseType: 'blob' })
  const url = window.URL.createObjectURL(new Blob([res.data]))
  const link = document.createElement('a')
  link.href = url
  link.setAttribute('download', 'olimpiada_natijalari.xlsx')
  document.body.appendChild(link)
  link.click()
  link.remove()
  window.URL.revokeObjectURL(url)
}

onMounted(async () => {
  await loadCurrentAdmin()
  await Promise.all([loadBranches(), loadCenters()])
  await loadResults()
})
</script>
