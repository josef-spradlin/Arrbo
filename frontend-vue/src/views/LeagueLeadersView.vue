<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { usePlayersStore } from '@/stores/players'
import type { EnrichedPlayer } from '@/types/dto'
import { getGames } from '@/api/arrbo'
import LeadersTable from '@/components/LeadersTable.vue'

type DayKey = 'today' | 'tomorrow'
type StatKey = 'projPts' | 'projReb' | 'projAst' | 'projPra'

const players = usePlayersStore()

const loading = ref(false)
const error = ref<string | null>(null)

const selectedDay = ref<DayKey>('today')
const selectedStat = ref<StatKey>('projPts')

const todayStr = new Date().toISOString().slice(0, 10)
const tomorrowStr = new Date(Date.now() + 86400000).toISOString().slice(0, 10)

const dayToDate = computed(() => (selectedDay.value === 'today' ? todayStr : tomorrowStr))

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

async function loadDay(day: DayKey) {
  try {
    loading.value = true
    error.value = null
    selectedDay.value = day

    await ensureProjectedPlayersForDate(day === 'today' ? todayStr : tomorrowStr)
  } catch (e: any) {
    error.value = e?.message ?? 'Failed to load league leaders'
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await loadDay('today')
})
</script>

<template>
  <div class="p-4">
    <div class="flex items-center justify-between mb-4">
      <h1 class="text-xl font-semibold">League Leaders</h1>
    </div>

    <div v-if="error" class="p-3 mb-4 border rounded">
      {{ error }}
    </div>

    <!-- Day toggle -->
    <div class="flex flex-wrap gap-2 mb-3">
      <button
        class="px-3 py-1 rounded border"
        :class="selectedDay === 'today' ? 'font-semibold' : ''"
        @click="loadDay('today')"
        :disabled="loading"
      >
        Today
      </button>

      <button
        class="px-3 py-1 rounded border"
        :class="selectedDay === 'tomorrow' ? 'font-semibold' : ''"
        @click="loadDay('tomorrow')"
        :disabled="loading"
      >
        Tomorrow
      </button>

      <div class="ml-auto text-sm opacity-70 self-center">
        Date: {{ dayToDate }}
      </div>
    </div>

    <!-- Stat toggle -->
    <div class="flex flex-wrap gap-2 mb-4">
      <button
        class="px-3 py-1 rounded border"
        :class="selectedStat === 'projPts' ? 'font-semibold' : ''"
        @click="selectedStat = 'projPts'"
      >
        PTS
      </button>

      <button
        class="px-3 py-1 rounded border"
        :class="selectedStat === 'projReb' ? 'font-semibold' : ''"
        @click="selectedStat = 'projReb'"
      >
        REB
      </button>

      <button
        class="px-3 py-1 rounded border"
        :class="selectedStat === 'projAst' ? 'font-semibold' : ''"
        @click="selectedStat = 'projAst'"
      >
        AST
      </button>

      <button
        class="px-3 py-1 rounded border"
        :class="selectedStat === 'projPra' ? 'font-semibold' : ''"
        @click="selectedStat = 'projPra'"
      >
        PRA
      </button>
    </div>

    <!-- Table -->
    <div v-if="loading" class="p-3 border rounded">Loading...</div>

    <div v-else class="border rounded p-3">
      <div class="font-semibold mb-3">
        Top 10 Projected {{ statLabel[selectedStat] }} — {{ selectedDay === 'today' ? 'Today' : 'Tomorrow' }}
      </div>

      <LeadersTable :rows="top10" :stat="selectedStat" />
    </div>
  </div>
</template>
