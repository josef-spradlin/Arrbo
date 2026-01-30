<script setup lang="ts">
import { computed, ref } from 'vue'
import { usePlayersStore } from '@/stores/players'

const players = usePlayersStore()

const TEAMS = [
  'ATL','BOS','BKN','CHA','CHI','CLE','DAL','DEN','DET','GSW','HOU','IND','LAC','LAL','MEM',
  'MIA','MIL','MIN','NOP','NYK','OKC','ORL','PHI','PHX','POR','SAC','SAS','TOR','UTA','WAS'
] as const

type HomeMode = 'TEAM_A' | 'TEAM_B' | 'NEUTRAL'

const teamA = ref<string>('BOS')
const teamB = ref<string>('LAL')
const homeMode = ref<HomeMode>('NEUTRAL')

// always use "today" internally for a fake game id
const today = new Date().toISOString().slice(0, 10)

const homeTeam = computed(() => {
  if (homeMode.value === 'TEAM_A') return teamA.value
  if (homeMode.value === 'TEAM_B') return teamB.value
  return teamA.value
})

const awayTeam = computed(() => {
  return homeTeam.value === teamA.value ? teamB.value : teamA.value
})

const neutralLabel = computed(() => {
  if (homeMode.value !== 'NEUTRAL') return ''
  return 'Neutral (no home team)'
})

async function run() {
  // prevent same-team selection
  if (teamA.value === teamB.value) return

  // This uses your existing store pipeline:
  // - ensureDataLoaded()
  // - build projections for the matchup
  await players.loadMatchup(homeTeam.value, awayTeam.value, today)
}
</script>

<template>
  <div class="p-4">
    <div class="flex items-center justify-between mb-4">
      <h1 class="text-xl font-semibold">Team Comparison</h1>
    </div>

    <!-- Controls -->
    <div class="border rounded p-3 mb-4">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div>
          <div class="text-sm font-semibold mb-1">Team A</div>
          <select v-model="teamA" class="border rounded w-full p-2">
            <option v-for="t in TEAMS" :key="t" :value="t">{{ t }}</option>
          </select>
        </div>

        <div>
          <div class="text-sm font-semibold mb-1">Team B</div>
          <select v-model="teamB" class="border rounded w-full p-2">
            <option v-for="t in TEAMS" :key="t" :value="t">{{ t }}</option>
          </select>
        </div>

        <div>
          <div class="text-sm font-semibold mb-1">Home / Neutral</div>
          <select v-model="homeMode" class="border rounded w-full p-2">
            <option value="NEUTRAL">Neutral</option>
            <option value="TEAM_A">Team A is Home</option>
            <option value="TEAM_B">Team B is Home</option>
          </select>
          <div v-if="neutralLabel" class="text-xs opacity-70 mt-1">{{ neutralLabel }}</div>
        </div>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 mt-3">
        <div class="md:col-span-2 flex items-end gap-2">
          <button class="px-3 py-2 rounded border"@click="run" :disabled="players.loading || teamA === teamB"> Generate </button>
          <div v-if="teamA === teamB" class="text-sm opacity-70">Pick two different teams.</div>
        </div>
      </div>
    </div>

    <!-- Status -->
    <div v-if="players.error" class="p-3 mb-4 border rounded">
      {{ players.error }}
    </div>
    <div v-if="players.loading" class="p-3 border rounded">Loading...</div>

    <!-- Results -->
    <div v-else-if="players.selectedGame" class="grid grid-cols-1 lg:grid-cols-2 gap-4">
      <!-- Insights -->
      <div class="border rounded p-3">
        <div class="font-semibold mb-2">
          Hypothetical Matchup: {{ players.selectedGame.awayTeamAbbr }} vs {{ players.selectedGame.homeTeamAbbr }}
        </div>
        <div class="text-sm opacity-70 mb-3">{{ players.selectedGame.gameDate }}</div>

        <div v-if="players.leaders" class="grid grid-cols-2 gap-3 text-sm">
          <div class="border rounded p-2">
            <div class="font-semibold mb-1">Top PTS</div>
            <div>{{ players.leaders.topPts?.playerName }} ({{ players.leaders.topPts?.teamAbbr }}) — {{ players.leaders.topPts?.projPts }}</div>
          </div>
          <div class="border rounded p-2">
            <div class="font-semibold mb-1">Top PRA</div>
            <div>{{ players.leaders.topPra?.playerName }} ({{ players.leaders.topPra?.teamAbbr }}) — {{ players.leaders.topPra?.projPra }}</div>
          </div>
          <div class="border rounded p-2">
            <div class="font-semibold mb-1">Top REB</div>
            <div>{{ players.leaders.topReb?.playerName }} ({{ players.leaders.topReb?.teamAbbr }}) — {{ players.leaders.topReb?.projReb }}</div>
          </div>
          <div class="border rounded p-2">
            <div class="font-semibold mb-1">Top AST</div>
            <div>{{ players.leaders.topAst?.playerName }} ({{ players.leaders.topAst?.teamAbbr }}) — {{ players.leaders.topAst?.projAst }}</div>
          </div>
        </div>

        <div v-else class="text-sm opacity-70">
          No leaders computed (no players).
        </div>
      </div>

      <!-- Projected Player Table -->
      <div class="border rounded p-3">
        <div class="font-semibold mb-2">Projected Players</div>

        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="border-b">
              <tr>
                <th class="text-left p-2">Team</th>
                <th class="text-left p-2">Opp</th>
                <th class="text-left p-2">Player</th>
                <th class="text-left p-2">Pos</th>
                <th class="text-right p-2">Usage%</th>
                <th class="text-right p-2">Proj PTS</th>
                <th class="text-right p-2">Proj REB</th>
                <th class="text-right p-2">Proj AST</th>
                <th class="text-right p-2">Proj PRA</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in players.matchupPlayers" :key="p.teamAbbr + p.playerName" class="border-b last:border-b-0">
                <td class="p-2">{{ p.teamAbbr }}</td>
                <td class="p-2">{{ p.opponentAbbr }}</td>
                <td class="p-2">{{ p.playerName }}</td>
                <td class="p-2">{{ p.position ?? '-' }}</td>
                <td class="p-2 text-right">{{ p.usagePct.toFixed(1) }}</td>
                <td class="p-2 text-right">{{ p.projPts.toFixed(1) }}</td>
                <td class="p-2 text-right">{{ p.projReb.toFixed(1) }}</td>
                <td class="p-2 text-right">{{ p.projAst.toFixed(1) }}</td>
                <td class="p-2 text-right">{{ p.projPra.toFixed(1) }}</td>
              </tr>

              <tr v-if="players.matchupPlayers.length === 0">
                <td colspan="9" class="p-3 text-center opacity-70">No players loaded.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <div v-else class="text-sm opacity-70">
      Pick two teams and click Generate.
    </div>
  </div>
</template>
