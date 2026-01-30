<template>
  <div class="min-h-screen bg-base-200 text-base-content">
    <!-- Navbar -->
    <header class="navbar bg-base-100 border-b border-base-300 sticky top-0 z-50">
      <div class="navbar-start gap-3">
        <img :src="logo" alt="Arrbo" class="h-12 w-12 rounded-2xl" />
        <div class="leading-tight">
          <div class="text-lg font-bold">Arrbo</div>
          <div class="text-xs opacity-70">NBA Analytics Comparison Model</div>
        </div>
      </div>

      <!-- Desktop tabs -->
      <div class="navbar-center hidden md:flex">
        <div class="tabs tabs-boxed">
          <RouterLink class="tab" :class="{ 'tab-active': activeTopTab === 'dashboard' }" to="/">
            Dashboard
          </RouterLink>

          <RouterLink
            class="tab"
            :class="{ 'tab-active': activeTopTab === 'leaders' }"
            to="/league-leaders"
          >
            League Leaders
          </RouterLink>

          <RouterLink
            class="tab"
            :class="{ 'tab-active': activeTopTab === 'compare' }"
            to="/team-comparison"
          >
            Team Comparison
          </RouterLink>
        </div>
      </div>

      <!-- Mobile menu -->
      <div class="navbar-end md:hidden">
        <div class="dropdown dropdown-end">
          <label tabindex="0" class="btn btn-ghost btn-square">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </label>

          <ul tabindex="0" class="menu dropdown-content mt-3 p-2 shadow bg-base-100 rounded-box w-52">
            <li>
              <RouterLink to="/" :class="{ active: activeTopTab === 'dashboard' }">Dashboard</RouterLink>
            </li>
            <li>
              <RouterLink to="/league-leaders" :class="{ active: activeTopTab === 'leaders' }">League Leaders</RouterLink>
            </li>
            <li>
              <RouterLink to="/team-comparison" :class="{ active: activeTopTab === 'compare' }">Team Comparison</RouterLink>
            </li>
          </ul>
        </div>
      </div>

      <!-- Repo link -->
      <div class="navbar-end hidden md:flex">
        <a class="btn btn-ghost btn-sm" href="https://github.com/josef-spradlin/Model" target="_blank" rel="noreferrer">
          Repo
        </a>
      </div>
    </header>

    <main class="max-w-7xl mx-auto p-4">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import logo from '@/assets/arrbo-logo.png'

const route = useRoute()

const activeTopTab = computed<'dashboard' | 'leaders' | 'compare'>(() => {
  const p = route.path

  if (p.startsWith('/league-leaders')) return 'leaders'
  if (p.startsWith('/team-comparison')) return 'compare'

  return 'dashboard'
})
</script>
