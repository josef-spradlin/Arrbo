<script setup lang="ts">
import { computed, ref } from 'vue'
import { usePlayersStore } from '@/stores/players'
import PlayerTable from '@/components/PlayerTable.vue'

const players = usePlayersStore()

const TEAMS = [
  'ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM',
  'MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS'
] as const

type HomeMode = 'NEUTRAL' | 'TEAM_A' | 'TEAM_B'

const teamA = ref<string>('BOS')
const teamB = ref<string>('LAL')
const homeMode = ref<HomeMode>('NEUTRAL')

const today = new Date().toISOString().slice(0, 10)

const computedHome = computed(() => {
  if (homeMode.value === 'TEAM_A') return teamA.value
  if (homeMode.value === 'TEAM_B') return teamB.value
  return teamA.value // neutral -> keep A in home slot for consistent layout
})

const computedAway = computed(() => (computedHome.value === teamA.value ? teamB.value : teamA.value))

const matchupLabel = computed(() => {
  if (homeMode.value === 'NEUTRAL') return `${teamA.value} vs ${teamB.value}`
  return `${computedAway.value} @ ${computedHome.value}`
})

const canRun = computed(() => teamA.value && teamB.value && teamA.value !== teamB.value)

async function run() {
  if (!canRun.value) return
  await players.loadMatchup(computedHome.value, computedAway.value, today)
}
</script>

<template>
  <div class="space-y-4">
    <!-- Header -->
    <div class="card bg-base-100 shadow">
      <div class="card-body p-4">
        <div class="flex items-start justify-between gap-3">
          <div>
            <h1 class="text-xl font-bold">Team Comparison</h1>
            <div class="text-sm opacity-70 mt-1">
              Generate a hypothetical matchup using current averages, usage, positions, and defensive efficiency.
            </div>
          </div>

          <div class="flex items-center gap-2">
            <span class="badge badge-outline">{{ matchupLabel }}</span>
            <span v-if="players.loading" class="loading loading-spinner loading-sm"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Controls -->
    <div class="card bg-base-100 shadow">
      <div class="card-body p-4 space-y-4">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div>
            <div class="text-sm font-semibold mb-1">Team A</div>
            <select v-model="teamA" class="select select-bordered w-full">
              <option v-for="t in TEAMS" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>

          <div>
            <div class="text-sm font-semibold mb-1">Team B</div>
            <select v-model="teamB" class="select select-bordered w-full">
              <option v-for="t in TEAMS" :key="t" :value="t">{{ t }}</option>
            </select>
          </div>

          <div>
            <div class="text-sm font-semibold mb-1">Home / Neutral</div>
            <div class="join w-full">
              <button
                class="btn join-item flex-1"
                :class="homeMode === 'NEUTRAL' ? 'btn-primary' : 'btn-ghost'"
                @click="homeMode = 'NEUTRAL'"
                type="button"
              >
                Neutral
              </button>
              <button
                class="btn join-item flex-1"
                :class="homeMode === 'TEAM_A' ? 'btn-primary' : 'btn-ghost'"
                @click="homeMode = 'TEAM_A'"
                type="button"
              >
                A Home
              </button>
              <button
                class="btn join-item flex-1"
                :class="homeMode === 'TEAM_B' ? 'btn-primary' : 'btn-ghost'"
                @click="homeMode = 'TEAM_B'"
                type="button"
              >
                B Home
              </button>
            </div>

            <div v-if="homeMode === 'NEUTRAL'" class="text-xs opacity-70 mt-2">
              Neutral site — Does not factor in Home Court Adjustment.
            </div>
          </div>
        </div>

        <div class="flex flex-wrap items-center gap-2">
          <button class="btn btn-primary w-full" @click="run" :disabled="players.loading || !canRun" type="button">
            Generate
          </button>

          <div v-if="!canRun" class="text-sm opacity-70">
            Pick two different teams.
          </div>
        </div>
      </div>
    </div>

    <!-- Error -->
    <div v-if="players.error" class="alert alert-error">
      <span>{{ players.error }}</span>
    </div>

    <!-- Results -->
    <div v-if="players.selectedGame && !players.loading" class="grid grid-cols-1 xl:grid-cols-3 gap-4">
      <!-- Leaders -->
      <div class="card bg-base-100 shadow xl:col-span-1">
        <div class="card-body p-4">
          <div class="flex items-center justify-between mb-2">
            <h2 class="card-title text-base">Insights</h2>
            <span class="badge badge-ghost">
              {{ players.selectedGame.awayTeamAbbr }} @ {{ players.selectedGame.homeTeamAbbr }}
            </span>
          </div>

          <div v-if="players.leaders" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-1 gap-3 text-sm">
            <div class="border border-base-300 rounded-xl p-3">
              <div class="font-semibold">Top PTS</div>
              <div class="opacity-80">
                {{ players.leaders.topPts?.playerName }} ({{ players.leaders.topPts?.teamAbbr }})
              </div>
              <div class="text-lg font-bold mt-1">
                {{ players.leaders.topPts?.projPts?.toFixed?.(1) }}
              </div>
            </div>

            <div class="border border-base-300 rounded-xl p-3">
              <div class="font-semibold">Top REB</div>
              <div class="opacity-80">
                {{ players.leaders.topReb?.playerName }} ({{ players.leaders.topReb?.teamAbbr }})
              </div>
              <div class="text-lg font-bold mt-1">
                {{ players.leaders.topReb?.projReb?.toFixed?.(1) }}
              </div>
            </div>

            <div class="border border-base-300 rounded-xl p-3">
              <div class="font-semibold">Top AST</div>
              <div class="opacity-80">
                {{ players.leaders.topAst?.playerName }} ({{ players.leaders.topAst?.teamAbbr }})
              </div>
              <div class="text-lg font-bold mt-1">
                {{ players.leaders.topAst?.projAst?.toFixed?.(1) }}
              </div>
            </div>

            <div class="border border-base-300 rounded-xl p-3">
              <div class="font-semibold">Top PRA</div>
              <div class="opacity-80">
                {{ players.leaders.topPra?.playerName }} ({{ players.leaders.topPra?.teamAbbr }})
              </div>
              <div class="text-lg font-bold mt-1">
                {{ players.leaders.topPra?.projPra?.toFixed?.(1) }}
              </div>
            </div>
          </div>

          <div v-else class="opacity-70">
            No leader projections available.
          </div>
        </div>
      </div>

      <!-- Table -->
      <div class="card bg-base-100 shadow xl:col-span-2">
        <div class="card-body p-4">
          <div class="flex items-center justify-between mb-2">
            <h2 class="card-title text-base">Projected Players</h2>
            <span class="badge badge-outline">{{ players.matchupPlayers.length }} players</span>
          </div>

          <PlayerTable :rows="players.matchupPlayers" />
        </div>
      </div>
    </div>

    <div v-else-if="players.loading" class="alert">
      <span>Building projections…</span>
    </div>

    <div v-else class="opacity-70">
      Pick two teams and click Generate.
    </div>
  </div>
</template>
