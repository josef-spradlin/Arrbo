<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { usePlayersStore } from '@/stores/players'
import type { EnrichedPlayer } from '@/types/dto'
import { getGames } from '@/api/arrbo'
import LeadersTable from '@/components/LeadersTable.vue'

type StatKey = 'projPts' | 'projReb' | 'projAst' | 'projPra'

const players = usePlayersStore()

const loading = ref(false)
const error = ref<string | null>(null)

// Toggle: false=today, true=tomorrow
const isTomorrow = ref(false)
const selectedStat = ref<StatKey>('projPts')

const todayStr = new Date().toISOString().slice(0, 10)
const tomorrowStr = new Date(Date.now() + 86400000).toISOString().slice(0, 10)

const dayToDate = computed(() => (isTomorrow.value ? tomorrowStr : todayStr))
const dayLabel = computed(() => (isTomorrow.value ? 'Tomorrow' : 'Today'))

const cache = ref<Record<string, EnrichedPlayer[]>>({})

const statLabel: Record<StatKey, string> = {
  projPts: 'PTS',
  projReb: 'REB',
  projAst: 'AST',
  projPra: 'PRA',
}

async function ensureProjectedPlayersForDate(date: string) {
  if (cache.value[date]) return
  await players.ensureDataLoaded()
  const games = await getGames(date)
  const allProjected = games.flatMap((g) => players.projectPlayersForGame(g))
  cache.value = { ...cache.value, [date]: allProjected }
}

const top10 = computed(() => {
  const date = dayToDate.value
  const rows = cache.value[date] ?? []
  const k = selectedStat.value
  return [...rows].sort((a, b) => (b[k] as number) - (a[k] as number)).slice(0, 10)
})

async function loadCurrentDay() {
  try {
    loading.value = true
    error.value = null
    await ensureProjectedPlayersForDate(dayToDate.value)
  } catch (e: any) {
    error.value = e?.message ?? 'Failed to load league leaders'
  } finally {
    loading.value = false
  }
}

watch(isTomorrow, async () => {
  await loadCurrentDay()
})

onMounted(async () => {
  await loadCurrentDay()
})
</script>

<template>
  <div class="space-y-4" data-testid="league-leaders-view">
    <!-- Header -->
    <div class="card bg-base-100 shadow">
      <div class="card-body p-4">
        <div class="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
          <div>
            <h1 class="text-xl font-bold" data-testid="league-leaders-title">Projected League Leaders</h1>
            <div class="text-sm opacity-70 mt-1">Top 10 projected performers across games.</div>
          </div>

          <div class="flex items-center gap-3">
            <span class="badge badge-ghost" data-testid="league-leaders-date-badge">Date: {{ dayToDate }}</span>

            <!-- Day toggle -->
            <div class="flex items-center gap-2">
              <span class="text-sm font-semibold" :class="!isTomorrow ? '' : 'opacity-60'">Today</span>

              <input
                data-testid="league-leaders-day-toggle"  
                type="checkbox"
                class="toggle toggle-primary"
                v-model="isTomorrow"
                aria-label="Toggle between today and tomorrow"
              />

              <span class="text-sm font-semibold" :class="isTomorrow ? '' : 'opacity-60'">Tomorrow</span>
            </div>
            <span v-if="loading" class="loading loading-spinner loading-sm" data-testid="league-leaders-loading-spinner"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-if="error" class="alert alert-error" data-testid="league-leaders-error">
      <span>{{ error }}</span>
    </div>

    <!-- Controls + Table -->
    <div class="card bg-base-100 shadow">
      <div class="card-body p-4 space-y-4">
        <!-- Stat selector as full-width segmented boxes -->
        <div class="grid grid-cols-2 md:grid-cols-4 gap-2">
          <button
              data-testid="league-leaders-stat-pts"
              type="button"
            class="btn"
            :class="selectedStat === 'projPts' ? 'btn-primary' : 'btn-ghost border border-base-300'"
            @click="selectedStat = 'projPts'"
          >
            PTS
          </button>

          <button
            data-testid="league-leaders-stat-reb"
            class="btn"
            :class="selectedStat === 'projReb' ? 'btn-primary' : 'btn-ghost border border-base-300'"
            @click="selectedStat = 'projReb'"
          >
            REB
          </button>

          <button
            data-testid="league-leaders-stat-ast"
            class="btn"
            :class="selectedStat === 'projAst' ? 'btn-primary' : 'btn-ghost border border-base-300'"
            @click="selectedStat = 'projAst'"
          >
            AST
          </button>

          <button
            data-testid="league-leaders-stat-pra"
            class="btn"
            :class="selectedStat === 'projPra' ? 'btn-primary' : 'btn-ghost border border-base-300'"
            @click="selectedStat = 'projPra'"
          >
            PRA
          </button>
        </div>

        <!-- Loading -->
        <div v-if="loading" class="alert" data-testid="league-leaders-loading">
          <span>Building projections…</span>
        </div>

        <!-- Table -->
        <div v-else class="space-y-2" data-testid="league-leaders-content">
          <div class="flex items-center justify-between">
            <div class="font-semibold">
              Top 10 Projected {{ statLabel[selectedStat] }}
              <span class="opacity-70">— {{ dayLabel }}</span>
            </div>
          </div>

          <div class="border border-base-300 rounded-xl overflow-hidden" data-testid="league-leaders-table">
            <LeadersTable :rows="top10" :stat="selectedStat" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
