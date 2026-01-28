<template>
  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px;">
    <section>
      <h2 style="margin: 0 0 8px;">Today ({{ today }})</h2>

      <div v-if="gamesStore.isLoading(today)">Loading...</div>
      <div v-else-if="gamesStore.error(today)" style="color: #b00020;">
        {{ gamesStore.error(today) }}
      </div>
      <GameList v-else :games="gamesStore.gamesForDate(today)" />
    </section>

    <section>
      <h2 style="margin: 0 0 8px;">Tomorrow ({{ tomorrow }})</h2>

      <div v-if="gamesStore.isLoading(tomorrow)">Loading...</div>
      <div v-else-if="gamesStore.error(tomorrow)" style="color: #b00020;">
        {{ gamesStore.error(tomorrow) }}
      </div>
      <GameList v-else :games="gamesStore.gamesForDate(tomorrow)" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import GameList from '../components/GameList.vue'
import { useGamesStore } from '../stores/games'

function formatLocalDateYYYYMMDD(d: Date): string {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

const gamesStore = useGamesStore()

const today = computed(() => formatLocalDateYYYYMMDD(new Date()))
const tomorrow = computed(() => {
  const d = new Date()
  d.setDate(d.getDate() + 1)
  return formatLocalDateYYYYMMDD(d)
})

onMounted(async () => {
  await Promise.all([
    gamesStore.fetchGames(today.value),
    gamesStore.fetchGames(tomorrow.value),
  ])
})
</script>
