<template>
  <div class="hacker-lab-page">
    <div class="page-head hacker-lab-head">
      <div>
        <h2>Hacker</h2>
        <p>Bu bo‘lim faqat vizual effekt uchun: matn yozilsa, terminal oynasida avtomatik dekorativ kodlar chiqadi.</p>
      </div>
      <button class="danger-btn" type="button" @click="clearTerminal">Terminalni tozalash</button>
    </div>

    <div class="hacker-lab-grid">
      <section class="panel hacker-type-panel">
        <span class="hacker-lab-label">INPUT // AUTO STREAM</span>
        <h3>Matn kiriting</h3>
        <textarea
          v-model="userText"
          rows="7"
          placeholder="Bu yerga istalgan narsa yozing..."
          @input="startStream"
        ></textarea>
        <div class="hacker-lab-actions">
          <button class="primary-btn" type="button" @click="startStream">▶ Kod yozishni boshlash</button>
          <button class="secondary-btn" type="button" @click="stopStream">⏸ To‘xtatish</button>
        </div>
        <div class="hacker-lab-mini">
          <span><b>{{ userText.length }}</b> belgi</span>
          <span><b>{{ codeLines.length }}</b> qator</span>
          <span :class="isStreaming ? 'online' : 'offline'"><i></i>{{ isStreaming ? 'AUTO WRITING' : 'PAUSED' }}</span>
        </div>
      </section>

      <section class="panel hacker-terminal-panel">
        <div class="terminal-window">
          <div class="terminal-top">
            <span class="dot red"></span>
            <span class="dot yellow"></span>
            <span class="dot green"></span>
            <b>al-aziz@academy:~/visual-hacker</b>
          </div>
          <div ref="terminalBody" class="terminal-body">
            <p v-for="(line, index) in codeLines" :key="index" :class="line.type">
              <span class="line-number">{{ String(index + 1).padStart(3, '0') }}</span>
              <code>{{ line.text }}</code>
            </p>
          </div>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'

const userText = ref('')
const terminalBody = ref(null)
const isStreaming = ref(false)
const codeLines = ref([
  { type: 'info', text: '[BOOT] AL-AZIZ VISUAL TERMINAL READY' },
  { type: 'ok', text: '[SYSTEM] type something to generate matrix-style code...' },
])
let timer = null
let cursor = 0

const safeSnippets = [
  text => `const input_${cursor} = "${escapeLine(text || 'AL_AZIZ')}";`,
  text => `render.matrixLine({ source: "${escapeLine(text || 'ADMIN')}", speed: ${random(12, 98)} });`,
  () => `ui.neonPulse("#00ff99", ${random(20, 90)});`,
  () => `console.stream("${randomHex(16)}", "${randomHex(16)}");`,
  () => `for (let i = 0; i < ${random(4, 18)}; i++) terminal.write(symbols[i]);`,
  () => `status.update({ panel: "ADMIN", mode: "VISUAL", code: "${randomHex(8)}" });`,
  () => `grid.scanLine(${random(100, 999)}, ${random(10, 88)});`,
  () => `effect.glow("terminal", { opacity: 0.${random(35, 95)}, blur: ${random(8, 32)} });`,
  text => `packet.preview("${escapeLine(text || 'OLIMPIADA')}") => ${randomHex(24)}`,
]

function escapeLine(value) {
  return String(value).replace(/[\\"`]/g, '').slice(-28) || 'AL_AZIZ'
}

function random(min, max) {
  return Math.floor(Math.random() * (max - min + 1)) + min
}

function randomHex(length) {
  const chars = 'ABCDEF0123456789'
  return Array.from({ length }, () => chars[random(0, chars.length - 1)]).join('')
}

function addLine() {
  const lastWords = userText.value.trim().split(/\s+/).filter(Boolean)
  const sample = lastWords.length ? lastWords[lastWords.length - 1] : 'AL_AZIZ'
  const maker = safeSnippets[cursor % safeSnippets.length]
  const type = cursor % 7 === 0 ? 'warn' : cursor % 5 === 0 ? 'ok' : 'code'
  codeLines.value.push({ type, text: maker(sample) })
  cursor += 1
  if (codeLines.value.length > 90) codeLines.value.splice(0, codeLines.value.length - 90)
  nextTick(() => {
    if (terminalBody.value) terminalBody.value.scrollTop = terminalBody.value.scrollHeight
  })
}

function startStream() {
  if (!userText.value.trim()) {
    codeLines.value.push({ type: 'warn', text: '[WAITING] avval matn kiriting...' })
    return
  }
  if (timer) return
  isStreaming.value = true
  addLine()
  timer = setInterval(addLine, 260)
}

function stopStream() {
  isStreaming.value = false
  if (timer) clearInterval(timer)
  timer = null
}

function clearTerminal() {
  stopStream()
  cursor = 0
  codeLines.value = [
    { type: 'info', text: '[CLEAR] terminal cleaned' },
    { type: 'ok', text: '[READY] yangi matn yozing...' },
  ]
}

watch(userText, value => {
  if (value.trim()) startStream()
  else stopStream()
})

onBeforeUnmount(stopStream)
</script>
