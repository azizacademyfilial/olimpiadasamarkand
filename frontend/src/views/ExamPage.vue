<template>
  <div class="exam-page" v-if="payload">
    <header class="exam-header">
      <div>
        <h1>{{ payload.student.full_name }}</h1>
        <p>{{ payload.student.subject_name }} / {{ payload.student.level_name }} / {{ payload.student.center_name }}</p>
      </div>
      <div v-if="!isMental" class="timer" :class="{ danger: remainingSeconds < 300 }">{{ formattedTime }}</div>
      <div v-else class="timer mental-timer" :class="{ danger: remainingSeconds < 60 }">
        {{ formattedTime }} · Mental {{ Math.min(currentMentalIndex + 1, mentalTasks.length) }}/{{ mentalTasks.length }}
      </div>
    </header>

    <main v-if="isMental" class="mental-stage">
      <div v-if="mentalPhase === 'countdown'" class="countdown-card">
        <p>Tayyorlaning</p>
        <strong>{{ countdownValue }}</strong>
      </div>

      <div v-else-if="mentalPhase === 'showing'" class="mental-number-card">
        <p>{{ currentMentalIndex + 1 }}-misol</p>
        <strong>{{ shownValue }}</strong>
        <span>Misol 3 sekund ko‘rsatiladi. Javob modalida ham vaqt davom etadi.</span>
      </div>

      <div v-else-if="mentalPhase === 'finished'" class="countdown-card">
        <p>Natija yuborilmoqda...</p>
      </div>

      <div class="mental-progress">
        <span v-for="(task, index) in mentalTasks" :key="task.id" :class="{ active: index === currentMentalIndex, done: mentalAnswers[task.id] !== undefined }"></span>
      </div>

      <div v-if="mentalPhase === 'answer'" class="modal-backdrop">
        <div class="answer-modal">
          <h2>{{ currentMentalIndex + 1 }}-misol javobi</h2>
          <p>Hisoblagan natijangizni kiriting.</p>
          <form @submit.prevent="saveMentalAnswer">
            <input ref="answerInputRef" v-model="answerInput" type="number" inputmode="numeric" placeholder="Javob" required />
            <button class="primary-btn" type="submit">Javobni saqlash</button>
          </form>
        </div>
      </div>

    </main>

    <main v-else class="exam-body">
      <div v-for="(q, index) in payload.questions" :key="q.id" class="question-card">
        <h3>{{ index + 1 }}. {{ q.text }}</h3>
        <div class="options-grid">
          <label v-for="opt in optionList(q)" :key="opt.value" class="option-card" :class="{ selected: answers[q.id] === opt.value }">
            <input type="radio" :name="`question-${q.id}`" :value="opt.value" v-model="answers[q.id]" @change="persistTestProgress" />
            <span>{{ opt.value }}) {{ opt.text }}</span>
          </label>
        </div>
      </div>
      <button class="primary-btn finish-btn" :disabled="submitting || finishModal.show" @click="submitExam">{{ submitting ? 'Yakunlanmoqda...' : 'Testni yakunlash' }}</button>
    </main>

    <div v-if="finishModal.show" class="modal-backdrop success-backdrop">
      <div class="finish-modal-card" :class="finishModal.type">
        <div class="finish-icon">{{ finishModal.type === 'success' ? '✓' : '!' }}</div>
        <h2>{{ finishModal.title }}</h2>
        <p>{{ finishModal.message }}</p>
        <div v-if="finishModal.result" class="student-result-box">
          <span>Sizning natijangiz</span>
          <strong>{{ finishModal.result.correct_count }}/{{ finishModal.result.total_questions }}</strong>
          <small>{{ finishModal.result.percent }}% to‘g‘ri javob</small>
        </div>
        <button class="primary-btn" type="button" @click="finishModal.type === 'success' ? goToStudentLogin() : closeFinishModal()">{{ finishModal.type === 'success' ? 'Code kiritish sahifasiga qaytish' : 'Yopish' }}</button>
      </div>
    </div>
  </div>
  <div v-else class="student-entry-page">
    <div class="student-card">
      <h1>Test topilmadi</h1>
      <RouterLink to="/student" class="primary-btn block-link">Code kiritish sahifasiga qaytish</RouterLink>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../api/axios'

const router = useRouter()
const payload = ref(null)
const answers = reactive({})
const remainingSeconds = ref(0)
const submitting = ref(false)
const finishModal = reactive({
  show: false,
  type: 'success',
  title: '',
  message: '',
  result: null,
})

const mentalPhase = ref('countdown')
const countdownValue = ref(3)
const currentMentalIndex = ref(0)
const shownValue = ref('')
const mentalAnswers = reactive({})
const answerInput = ref('')
const answerInputRef = ref(null)
const mentalTimers = []

let intervalId = null
let submitted = false
let progressSaveTimer = null
let lastServerProgressSave = 0
let timerTicksSinceServerSave = 0

const isMental = computed(() => payload.value?.mode === 'mental')
const mentalTasks = computed(() => payload.value?.mental_tasks || [])
const formattedTime = computed(() => {
  const m = Math.floor(remainingSeconds.value / 60)
  const s = remainingSeconds.value % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})

function showFinishSuccess(result) {
  finishModal.show = true
  finishModal.type = 'success'
  finishModal.title = isMental.value ? 'Mental arifmetika yakunlandi' : 'Test muvaffaqiyatli yakunlandi'
  if (isMental.value && result) {
    finishModal.message = `Siz ${result.total_questions} tadan ${result.correct_count} tasini to‘g‘ri ishladingiz.`
  } else {
    finishModal.message = 'Javoblaringiz adminga yuborildi. To‘g‘ri javoblar kaliti ko‘rsatilmaydi.'
  }
  finishModal.result = result || null
}

function showFinishError(message) {
  finishModal.show = true
  finishModal.type = 'error'
  finishModal.title = 'Xatolik yuz berdi'
  finishModal.message = message || 'Javoblarni yuborishda xatolik yuz berdi.'
  finishModal.result = null
}

function goToStudentLogin() {
  router.push('/student')
}

function closeFinishModal() {
  finishModal.show = false
}

function optionList(q) {
  return [
    { value: 'A', text: q.option_a },
    { value: 'B', text: q.option_b },
    { value: 'C', text: q.option_c },
    { value: 'D', text: q.option_d },
  ]
}

function payloadCode() {
  return payload.value?.code || payload.value?.student?.code || ''
}

function examProgressKey() {
  const code = payloadCode()
  return code ? `exam_progress_${code}` : ''
}

function buildProgressBody() {
  return {
    code: payloadCode(),
    remaining_seconds: Math.max(0, Number(remainingSeconds.value || 0)),
    current_index: isMental.value ? Number(currentMentalIndex.value || 0) : 0,
    answers: isMental.value ? { ...mentalAnswers } : { ...answers },
  }
}

async function saveProgressToServer(force = false) {
  if (!payload.value || submitted || !payloadCode()) return
  const now = Date.now()
  if (!force && now - lastServerProgressSave < 2500) return
  lastServerProgressSave = now
  try {
    await api.post('/exam/progress/', buildProgressBody())
  } catch (_) {}
}

function scheduleProgressSave() {
  if (!payload.value || submitted) return
  if (progressSaveTimer) clearTimeout(progressSaveTimer)
  progressSaveTimer = setTimeout(() => {
    progressSaveTimer = null
    saveProgressToServer(true)
  }, 400)
}

function persistTestProgress(sendRemote = true) {
  const key = examProgressKey()
  if (!key) return
  localStorage.setItem(key, JSON.stringify({ answers: { ...answers }, remaining_seconds: remainingSeconds.value }))
  if (sendRemote !== false) scheduleProgressSave()
}

function loadTestProgress() {
  const serverAnswers = payload.value?.saved_answers
  if (serverAnswers && typeof serverAnswers === 'object') {
    Object.assign(answers, serverAnswers)
  }

  const key = examProgressKey()
  if (!key) return
  try {
    const saved = JSON.parse(localStorage.getItem(key) || '{}')
    if (saved.answers && typeof saved.answers === 'object') {
      Object.assign(answers, saved.answers)
    }
  } catch (_) {}
}

function safeDurationMinutes(defaultMinutes) {
  if (isMental.value) return 5
  const value = Number(defaultMinutes)
  return Number.isFinite(value) && value > 0 ? value : 30
}

function remainingFromStartedAt(defaultMinutes) {
  const minutes = safeDurationMinutes(defaultMinutes)
  const durationSeconds = Math.max(1, minutes * 60)
  const savedRemaining = Number(payload.value?.remaining_seconds)
  if (Number.isFinite(savedRemaining) && savedRemaining >= 0) {
    return Math.max(0, Math.min(durationSeconds, Math.floor(savedRemaining)))
  }

  // Backend yangi test boshlanganda resume=false yuboradi.
  // Shunda yangi yaratilgan o‘quvchi 00:00 bo‘lib qolmaydi, 30:00 dan boshlaydi.
  if (payload.value?.resume === false) {
    return durationSeconds
  }

  const startedAt = Date.parse(payload.value?.started_at || '')
  if (!Number.isFinite(startedAt)) {
    return durationSeconds
  }

  const elapsedSeconds = Math.max(0, Math.floor((Date.now() - startedAt) / 1000))
  return Math.max(0, durationSeconds - elapsedSeconds)
}

function clearMentalTimers() {
  while (mentalTimers.length) clearTimeout(mentalTimers.pop())
}

function mentalProgressKey() {
  const code = payloadCode()
  return code ? `mental_progress_${code}` : ''
}

function persistMentalProgress(sendRemote = true) {
  const key = mentalProgressKey()
  if (!key) return
  localStorage.setItem(key, JSON.stringify({
    answers: { ...mentalAnswers },
    remaining_seconds: remainingSeconds.value,
    current_index: currentMentalIndex.value,
  }))
  if (sendRemote !== false) scheduleProgressSave()
}

function loadMentalProgress() {
  const serverAnswers = payload.value?.saved_answers
  if (serverAnswers && typeof serverAnswers === 'object') {
    Object.assign(mentalAnswers, serverAnswers)
  }

  const key = mentalProgressKey()
  try {
    if (key) {
      const saved = JSON.parse(localStorage.getItem(key) || '{}')
      if (saved.answers && typeof saved.answers === 'object') {
        Object.assign(mentalAnswers, saved.answers)
      }
    }
    const firstUnansweredIndex = mentalTasks.value.findIndex(task => mentalAnswers[task.id] === undefined)
    const serverIndex = Number(payload.value?.progress_current_index || 0)
    currentMentalIndex.value = firstUnansweredIndex === -1
      ? mentalTasks.value.length
      : Math.max(0, Math.min(firstUnansweredIndex, Number.isFinite(serverIndex) ? serverIndex : firstUnansweredIndex))
  } catch (_) {
    currentMentalIndex.value = 0
  }
}

function startMentalCountdown(startIndex = 0) {
  mentalPhase.value = 'countdown'
  countdownValue.value = 3
  const tick = () => {
    if (countdownValue.value <= 1) {
      playMentalTask(startIndex)
      return
    }
    countdownValue.value -= 1
    mentalTimers.push(setTimeout(tick, 1000))
  }
  mentalTimers.push(setTimeout(tick, 1000))
}

function playMentalTask(index) {
  clearMentalTimers()
  const task = mentalTasks.value[index]
  if (!task) {
    submitMentalExam()
    return
  }

  currentMentalIndex.value = index
  mentalPhase.value = 'showing'
  shownValue.value = ''
  answerInput.value = ''

  const flashes = task.flashes || []
  const taskDisplayMs = Number(task.task_display_ms || 3000)
  const perFlashMs = flashes.length ? Math.max(250, Math.floor(taskDisplayMs / flashes.length)) : taskDisplayMs

  flashes.forEach((value, flashIndex) => {
    mentalTimers.push(setTimeout(() => {
      shownValue.value = value
    }, flashIndex * perFlashMs))
  })

  mentalTimers.push(setTimeout(async () => {
    mentalPhase.value = 'answer'
    shownValue.value = ''
    await nextTick()
    answerInputRef.value?.focus()
  }, taskDisplayMs))
}

function saveMentalAnswer() {
  const task = mentalTasks.value[currentMentalIndex.value]
  if (!task) return

  mentalAnswers[task.id] = answerInput.value
  persistMentalProgress()

  const nextIndex = currentMentalIndex.value + 1
  if (remainingSeconds.value <= 0 || nextIndex >= mentalTasks.value.length) {
    submitMentalExam()
  } else {
    playMentalTask(nextIndex)
  }
}

async function submitMentalExam() {
  if (submitted || !payload.value) return
  submitted = true
  submitting.value = true
  mentalPhase.value = 'finished'
  clearMentalTimers()

  const lastAttemptedIndex = Math.min(currentMentalIndex.value, mentalTasks.value.length - 1)
  const answerList = mentalTasks.value
    .filter((task, index) => index <= lastAttemptedIndex || mentalAnswers[task.id] !== undefined)
    .map(task => ({
      task_id: task.id,
      answer: mentalAnswers[task.id] ?? '',
    }))

  try {
    const res = await api.post('/exam/submit/', { code: payloadCode(), answers: answerList })
    sessionStorage.removeItem('exam_payload')
    localStorage.removeItem(mentalProgressKey())
    localStorage.removeItem(examProgressKey())
    showFinishSuccess(res.data)
  } catch (e) {
    submitted = false
    showFinishError(e.response?.data?.detail || 'Mental javoblarni yuborishda xatolik.')
  } finally {
    submitting.value = false
  }
}

async function submitExam() {
  if (submitted || !payload.value) return
  submitted = true
  submitting.value = true
  clearInterval(intervalId)
  const answerList = payload.value.questions.map(q => ({ question_id: q.id, answer: answers[q.id] || '' }))
  try {
    const res = await api.post('/exam/submit/', { code: payloadCode(), answers: answerList })
    sessionStorage.removeItem('exam_payload')
    localStorage.removeItem(examProgressKey())
    localStorage.removeItem(mentalProgressKey())
    showFinishSuccess(res.data)
  } catch (e) {
    submitted = false
    showFinishError(e.response?.data?.detail || 'Testni yakunlashda xatolik.')
  } finally {
    submitting.value = false
  }
}

function startTimer() {
  clearInterval(intervalId)
  intervalId = setInterval(() => {
    if (submitted) {
      clearInterval(intervalId)
      return
    }

    // Vaqt backenddagi started_at bo‘yicha hisoblanadi; bu yerda faqat ekrandagi timer yuradi.
    // Javoblar localStorage’da saqlanadi, code qayta kiritilganda boshidan boshlanmaydi.
    remainingSeconds.value = Math.max(0, remainingSeconds.value - 1)
    if (isMental.value) persistMentalProgress(false)
    else persistTestProgress(false)

    timerTicksSinceServerSave += 1
    if (timerTicksSinceServerSave >= 3) {
      timerTicksSinceServerSave = 0
      saveProgressToServer(false)
    }

    if (remainingSeconds.value <= 0) {
      remainingSeconds.value = 0
      clearInterval(intervalId)
      clearMentalTimers()
      if (isMental.value) submitMentalExam()
      else submitExam()
    }
  }, 1000)
}

function saveProgressBeforeExit() {
  if (!payload.value || submitted) return
  if (isMental.value) persistMentalProgress(false)
  else persistTestProgress(false)

  try {
    const body = JSON.stringify(buildProgressBody())
    fetch(`${api.defaults.baseURL}/exam/progress/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body,
      keepalive: true,
    })
  } catch (_) {}
}

onMounted(() => {
  window.addEventListener('beforeunload', saveProgressBeforeExit)
  window.addEventListener('pagehide', saveProgressBeforeExit)
  const saved = sessionStorage.getItem('exam_payload')
  if (!saved) return
  payload.value = JSON.parse(saved)

  if (isMental.value) {
    // Mentalda code qayta kiritilganda vaqt yangidan boshlanmaydi.
    // Backend bergan started_at bo‘yicha qolgan vaqt hisoblanadi.
    const durationMinutes = safeDurationMinutes(payload.value.duration_minutes || 5)
    remainingSeconds.value = remainingFromStartedAt(durationMinutes)

    loadMentalProgress()
    if (remainingSeconds.value <= 0 || currentMentalIndex.value >= mentalTasks.value.length) {
      submitMentalExam()
    } else {
      startTimer()
      startMentalCountdown(currentMentalIndex.value)
    }
    return
  }

  // Oddiy testda 30 minut vaqt beriladi. Code qayta kiritilganda avvalgi javoblar va qolgan vaqt saqlanadi.
  const durationMinutes = safeDurationMinutes(payload.value.duration_minutes || 30)
  remainingSeconds.value = remainingFromStartedAt(durationMinutes)
  loadTestProgress()

  if (remainingSeconds.value <= 0) {
    submitExam()
  } else {
    startTimer()
  }
})

onBeforeUnmount(() => {
  saveProgressBeforeExit()
  window.removeEventListener('beforeunload', saveProgressBeforeExit)
  window.removeEventListener('pagehide', saveProgressBeforeExit)
  clearInterval(intervalId)
  if (progressSaveTimer) clearTimeout(progressSaveTimer)
  clearMentalTimers()
})
</script>
