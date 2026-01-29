<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useGamesStore } from '@/stores/games'
import { usePlayersStore } from '@/stores/players'
import GameList from '@/components/GameList.vue'
import MatchupCard from '@/components/MatchupCard.vue'
import PlayerTable from '@/components/PlayerTable.vue'

function yyyyMmDd(d: Date) {
  const y = d.getFullYear()
  const m = String(d.getMonth() + 1).padStart(2, '0')
  const day = String(d.getDate()).padStart(2, '0')
  return `${y}-${m}-${day}`
}

const gamesStore = useGamesStore()
const playersStore = usePlayersStore()

const today = ref(yyyyMmDd(new Date()))
const tomorrow = ref(yyyyMmDd(new Date(Date.now() + 24 * 60 * 60 * 1000)))

onMounted(async () => {
  await Promise.all([gamesStore.load(today.value), gamesStore.load(tomorrow.value)])
})

const todayGames = computed(() => gamesStore.gamesByDate[today.value] ?? [])
const tomorrowGames = computed(() => gamesStore.gamesByDate[tomorrow.value] ?? [])

async function onSelectGame(game: any) {
  await playersStore.selectGame(game)
}
</script>

<template>
  <div style="display: grid; grid-template-columns: 320px 1fr; gap: 16px; padding: 16px;">
    <div>
      <h2>Today ({{ today }})</h2>
      <GameList :games="todayGames" @select="onSelectGame" />

      <h2 style="margin-top: 16px;">Tomorrow ({{ tomorrow }})</h2>
      <GameList :games="tomorrowGames" @select="onSelectGame" />

      <div v-if="gamesStore.error" style="color: red; margin-top: 12px;">
        {{ gamesStore.error }}
      </div>
    </div>

    <div>
      <h2>Matchup Insights</h2>

      <div v-if="!playersStore.selectedGame" style="opacity: 0.7;">
        Click a game to generate predictions.
      </div>

      <div v-else>
        <MatchupCard
          :game="playersStore.selectedGame"
          :leaders="playersStore.leaders"
          :loading="playersStore.loading"
          :error="playersStore.error"
        />

        <h3 style="margin-top: 16px;">Projected Player Table</h3>
        <PlayerTable :rows="playersStore.matchupPlayers" />
      </div>
    </div>
  </div>
</template>
