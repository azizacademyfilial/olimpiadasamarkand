<template>
  <div class="admin-shell">
    <aside class="sidebar" :class="{ open: menuOpen }">
      <div class="sidebar-brand">
        <div class="brand-circle small brand-icon-only">🏆</div>
        <div>
          <h2>AZIZ ACADEMY PLATFORM</h2>
          <span>{{ adminTitle }}</span>
        </div>
      </div>

      <nav @click="menuOpen = false">
        <RouterLink to="/admin/dashboard">Dashboard</RouterLink>
        <RouterLink v-if="mainAdmin" to="/admin/admins">Adminlar</RouterLink>
        <RouterLink v-if="currentAdmin?.can_create_students" to="/admin/students/create">O‘quvchi yaratish</RouterLink>
        <RouterLink v-if="currentAdmin?.can_create_students" to="/admin/students/import">Excel yuklash</RouterLink>
        <RouterLink to="/admin/students">Yaratilgan o‘quvchilar</RouterLink>
        <RouterLink to="/admin/questions">Testlar</RouterLink>
        <RouterLink to="/admin/results">Natijalar</RouterLink>
        <RouterLink to="/admin/mental-answers">Mental javoblari</RouterLink>
      </nav>

      <button class="ghost-btn logout" @click="logout">Chiqish</button>
    </aside>

    <main class="admin-main">
      <header class="topbar">
        <button class="menu-btn" @click="menuOpen = !menuOpen">☰</button>
        <div>
          <h1>Al-Aziz Academy</h1>
          <p v-if="mainAdmin">Al-Aziz Academy admin paneli va natijalar boshqaruvi</p>
          <p v-else>{{ adminTitle }} o‘quvchilari va natijalari</p>
        </div>
        <RouterLink to="/student" class="student-link">O‘quvchi kirishi</RouterLink>
      </header>

      <section class="content-wrap">
        <RouterView />
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { clearAuthStorage, fetchCurrentAdmin, getStoredAdminProfile, isMainAdmin } from '../utils/auth'

const router = useRouter()
const menuOpen = ref(false)
const currentAdmin = ref(getStoredAdminProfile())
const mainAdmin = computed(() => isMainAdmin(currentAdmin.value))
const adminTitle = computed(() => currentAdmin.value?.center_name || currentAdmin.value?.assigned_center_name || currentAdmin.value?.branch || 'Bosh admin')

function logout() {
  clearAuthStorage()
  router.push('/admin/login')
}

onMounted(async () => {
  try {
    currentAdmin.value = await fetchCurrentAdmin()
  } catch {
    clearAuthStorage()
    router.push('/admin/login')
  }
})
</script>
