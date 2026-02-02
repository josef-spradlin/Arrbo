<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
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

//Toggle: false = today, true = tomorrow
const isTomorrow = ref(false)

const dayLabel = computed(() => (isTomorrow.value ? 'Tomorrow' : 'Today'))
const dayDate = computed(() => (isTomorrow.value ? tomorrow.value : today.value))

const todayGames = computed(() => gamesStore.gamesByDate[today.value] ?? [])
const tomorrowGames = computed(() => gamesStore.gamesByDate[tomorrow.value] ?? [])

const dayGames = computed(() => (isTomorrow.value ? tomorrowGames.value : todayGames.value))

async function selectGameSafe(game: any | undefined) {
  if (!game) return
  if (playersStore.selectedGame?.gameId === game.gameId) return
  await playersStore.selectGame(game)
}


async function autoSelectFirstGameForCurrentDay() {
  const list = dayGames.value
  if (list.length > 0) {
    await selectGameSafe(list[0])
  } else {
    // no games => clear selection
    playersStore.selectedGame = null
    playersStore.matchupPlayers = []
    playersStore.leaders = null
    playersStore.error = null
  }
}

onMounted(async () => {
  await Promise.all([gamesStore.load(today.value), gamesStore.load(tomorrow.value)])
  // always show something immediately
  await autoSelectFirstGameForCurrentDay()
})

// when toggle changes, select first game of that day
watch(isTomorrow, async () => {
  await autoSelectFirstGameForCurrentDay()
})

async function onSelectGame(game: any) {
  await playersStore.selectGame(game)
}
</script>

<template>
  <div class="space-y-4" data-testid="dashboard-view">
    <!-- Header + Toggle -->
    <div class="card bg-base-100 shadow">
      <div class="card-body p-4">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
          <div>
            <h1 class="text-xl font-bold">Dashboard</h1>
            <div class="text-sm opacity-70">
              Toggle day → click a game → view matchup projections.
            </div>
          </div>

          <div class="flex items-center gap-3">
            <span class="badge badge-ghost" data-testid="date-badge">Date: {{ dayDate }}</span>

            <!-- Toggle switch -->
            <div class="flex items-center gap-2">
              <span class="text-sm font-semibold" :class="!isTomorrow ? '' : 'opacity-60'">Today</span>

              <input
                data-testid="day-toggle"  
                type="checkbox"
                class="toggle toggle-primary"
                v-model="isTomorrow"
                aria-label="Toggle between today and tomorrow"
              />

              <span class="text-sm font-semibold" :class="isTomorrow ? '' : 'opacity-60'">Tomorrow</span>
            </div>
          </div>
        </div>

        <div v-if="gamesStore.error" class="alert alert-error mt-4">
          <span>{{ gamesStore.error }}</span>
        </div>
      </div>
    </div>

    <!-- Main: left list + right insights -->
    <div class="grid grid-cols-1 lg:grid-cols-[360px_1fr] gap-4">
      <!-- LEFT -->
      <div class="card bg-base-100 shadow">
        <div class="card-body p-4">
          <div class="flex items-center justify-between mb-2">
            <h2 class="card-title text-base">{{ dayLabel }} Games</h2>
            <span class="badge badge-outline" data-testid="day-games-count">{{ dayGames.length }}</span>
          </div>

          <GameList :games="dayGames" :selectedGameId="playersStore.selectedGame?.gameId" @select="onSelectGame"/>

        </div>
      </div>

      <!-- RIGHT -->
      <div class="card bg-base-100 shadow">
        <div class="card-body p-4">
          <div class="flex items-center justify-between">
            <h2 class="card-title">Matchup Insights</h2>

            <div class="flex items-center gap-2">
              <span v-if="playersStore.loading" data-testid="players-loading" class="loading loading-spinner loading-sm"></span>

              <span v-if="playersStore.selectedGame" class="badge badge-outline" data-testid="selected-matchup-badge">
                {{ playersStore.selectedGame.awayTeamAbbr }} @ {{ playersStore.selectedGame.homeTeamAbbr }}
              </span>
            </div>
          </div>

          <div v-if="!playersStore.selectedGame" class="opacity-70 mt-2" data-testid="no-games-message">
            No games loaded for {{ dayLabel.toLowerCase() }}.
          </div>

          <div v-else class="mt-3">
            <MatchupCard
              :game="playersStore.selectedGame"
              :leaders="playersStore.leaders"
              :loading="playersStore.loading"
              :error="playersStore.error"
            />
          </div>
        </div>
      </div>
    </div>

    <!-- Bottom table -->
    <div class="card bg-base-100 shadow" data-testid="player-table-card">
      <div class="card-body p-4">
        <div class="flex items-center justify-between mb-2">
          <h3 class="card-title text-base">Projected Player Table</h3>
          <span class="badge badge-ghost">{{ playersStore.matchupPlayers.length }} players</span>
        </div>

        <div v-if="!playersStore.selectedGame" class="opacity-70 text-sm">
          No matchup selected.
        </div>

        <div v-else data-testid="player-table">
          <PlayerTable :rows="playersStore.matchupPlayers" />
        </div>
      </div>
    </div>
  </div>
</template>
