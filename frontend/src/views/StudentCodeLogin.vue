<template>
  <div class="student-entry-page olympiad-entry world-entry">
    <div class="entry-orb entry-orb-one"></div>
    <div class="entry-orb entry-orb-two"></div>
    <div class="entry-orb entry-orb-three"></div>

    <section class="world-hero-shell">
      <div class="world-hero-copy">
        <div class="world-brand-line no-mark">
          <div>
            <span class="entry-badge">Al-Aziz Academy Contest</span>
            <h1>Al-Aziz Academy</h1>
          </div>
        </div>

        <p class="entry-subtitle world-subtitle">
          Al-Aziz Academy o‘quvchilari uchun zamonaviy online test platformasi. Status code orqali testga kiring,
          topshiriqlarni bajaring va natijangizni tezkor tekshiring.
        </p>

        <div class="world-feature-grid">
          <span>⚡ Tezkor kirish</span>
          <span>🏆 Al-Aziz Academy testlari</span>
          <span>📊 Natija ko‘rish</span>
        </div>
      </div>

      <div class="student-card entry-card world-login-card">
        <div class="entry-top compact">
          <span class="entry-badge">Student access</span>
        </div>

        <h2>Testga kirish</h2>
        <p class="entry-subtitle">Admin bergan 6 xonali status code’ni kiriting.</p>

        <form @submit.prevent="startExam" class="code-form entry-form">
          <label class="code-label">
            Status code
            <input
              v-model="code"
              maxlength="6"
              minlength="6"
              inputmode="numeric"
              placeholder="582914"
              required
            />
          </label>
          <button class="primary-btn entry-start-btn" :disabled="loading">
            {{ loading ? 'Tekshirilmoqda...' : 'Testni boshlash' }}
          </button>
        </form>

        <p v-if="error" class="error-box">{{ error }}</p>

        <RouterLink to="/admin/login" class="admin-login-link entry-admin-link">
          Admin panelga kirish
        </RouterLink>
      </div>
    </section>

    <div v-if="showResultModal" class="modal-backdrop result-lookup-backdrop" @click.self="closeResultModal">
      <div class="answer-modal result-lookup-modal">
        <button type="button" class="modal-close-btn" @click="closeResultModal">×</button>

        <template v-if="!publicResult">
          <div class="result-modal-icon">📊</div>
          <h2>Natijani ko‘rish</h2>
          <p>Natijangizni ko‘rish uchun sizga berilgan 6 xonali status code’ni kiriting.</p>

          <form @submit.prevent="lookupResult" class="result-lookup-form">
            <label class="code-label">
              Status code
              <input
                v-model="resultCode"
                maxlength="6"
                minlength="6"
                inputmode="numeric"
                placeholder="582914"
                required
              />
            </label>
            <button class="primary-btn" :disabled="resultLoading">
              {{ resultLoading ? 'Qidirilmoqda...' : 'Natijani ko‘rish' }}
            </button>
          </form>

          <p v-if="resultError" class="error-box">{{ resultError }}</p>
        </template>

        <template v-else>
          <div class="result-modal-icon success">✓</div>
          <h2>{{ publicResult.student_full_name }}</h2>
          <p class="result-meta">
            {{ publicResult.subject_name }} · {{ publicResult.level_name }}
          </p>

          <div class="public-result-score">
            <span>Natija</span>
            <strong>{{ publicResult.correct_count }}/{{ publicResult.total_questions }}</strong>
            <small>{{ publicResult.total_questions }} tadan {{ publicResult.correct_count }} ta to‘g‘ri</small>
          </div>

          <div class="public-result-details">
            <div>
              <span>Foiz</span>
              <b>{{ publicResult.percent }}%</b>
            </div>
            <div>
              <span>O‘quv markaz</span>
              <b>{{ publicResult.center_name }}</b>
            </div>
            <div>
              <span>Filial</span>
              <b>{{ publicResult.branch || '—' }}</b>
            </div>
            <div>
              <span>Sarflagan vaqt</span>
              <b>{{ formatSeconds(publicResult.spent_seconds) }}</b>
            </div>
          </div>

          <div v-if="publicResult.is_mental && publicResult.mental_answers?.length" class="public-mental-breakdown">
            <h3>Mental javoblaringiz</h3>
            <div class="public-mental-list">
              <span v-for="item in publicResult.mental_answers" :key="item.id" :class="item.is_correct ? 'ok' : 'bad'">
                {{ item.task_order }}. {{ item.expression }} = {{ item.student_answer ?? '—' }}
                <b>{{ item.is_correct ? 'To‘g‘ri' : 'Noto‘g‘ri' }}</b>
              </span>
            </div>
          </div>

          <button type="button" class="secondary-btn block-link" @click="resetResultLookup">
            Boshqa code tekshirish
          </button>
        </template>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/axios'

const router = useRouter()
const code = ref('')
const loading = ref(false)
const error = ref('')
const showResultModal = ref(false)
const resultCode = ref('')
const resultLoading = ref(false)
const resultError = ref('')
const publicResult = ref(null)

function cleanCode(value) {
  return String(value || '').trim()
}

function formatSeconds(seconds) {
  const total = Number(seconds || 0)
  const min = Math.floor(total / 60)
  const sec = total % 60
  return `${min} daq ${sec} sek`
}

function openResultModal() {
  showResultModal.value = true
  resultCode.value = cleanCode(code.value)
  resultError.value = ''
  publicResult.value = null
}

function closeResultModal() {
  showResultModal.value = false
}

function resetResultLookup() {
  publicResult.value = null
  resultCode.value = ''
  resultError.value = ''
}

async function startExam() {
  loading.value = true
  error.value = ''
  try {
    const finalCode = cleanCode(code.value)
    const res = await api.post('/exam/start/', { code: finalCode })
    sessionStorage.setItem('exam_payload', JSON.stringify({ ...res.data, code: finalCode }))
    router.push('/exam')
  } catch (e) {
    error.value = e.response?.data?.detail || 'Code xato yoki oldin ishlatilgan.'
  } finally {
    loading.value = false
  }
}

async function lookupResult() {
  resultLoading.value = true
  resultError.value = ''
  publicResult.value = null
  try {
    const res = await api.post('/exam/result/', { code: cleanCode(resultCode.value) })
    publicResult.value = res.data
  } catch (e) {
    resultError.value = e.response?.data?.detail || 'Natija topilmadi.'
  } finally {
    resultLoading.value = false
  }
}
</script>
