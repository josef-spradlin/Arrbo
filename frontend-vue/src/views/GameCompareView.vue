<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { usePlayersStore } from '@/stores/players'
import PlayerTable from '@/components/PlayerTable.vue'

const props = defineProps<{
  gameId: string
  home?: string
  away?: string
  date?: string
}>()

const players = usePlayersStore()

onMounted(async () => {
  if (props.home && props.away) {
    await players.loadMatchup(String(props.home), String(props.away), props.date)
  }
})

const leaders = computed(() => players.leaders)
</script>

<template>
  <div class="space-y-4" data-testid="game-compare-view">
    <!-- Header -->
    <div class="card bg-base-100 shadow">
      <div class="card-body p-4">
        <div class="flex items-start justify-between gap-3">
          <div>
            <h1 class="text-xl font-bold" data-testid="game-compare-title">Game Compare</h1>
            <div class="text-sm opacity-70 mt-1">
              Game ID: <span class="font-mono" data-testid="game-compare-game-id">{{ gameId }}</span>
            </div>
          </div>

          <div class="flex flex-wrap items-center gap-2">
            <span v-if="away && home" class="badge badge-outline" data-testid="game-compare-matchup-badge">
              {{ away }} @ {{ home }}
            </span>
            <span v-if="date" class="badge badge-ghost" data-testid="game-compare-date-badge">{{ date }}</span>
            <span v-if="players.loading" class="loading loading-spinner loading-sm" data-testid="game-compare-loading-spinner"></span>
          </div>
        </div>
      </div>
    </div>

    <!-- Loading / Error -->
    <div v-if="players.loading" class="alert" data-testid="game-compare-loading">
      <span>Loading matchup data...</span>
    </div>

    <div v-else-if="players.error" class="alert alert-error" data-testid="game-compare-error">
      <span>{{ players.error }}</span>
    </div>

    <!-- Content -->
    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-4" data-testid="game-compare-content">
      <!-- Leaders -->
      <div class="card bg-base-100 shadow" data-testid="game-compare-leaders-card">
        <div class="card-body p-4">
          <div class="flex items-center justify-between mb-2">
            <h2 class="card-title text-base">Predicted Leaders</h2>
            <span v-if="leaders" class="badge badge-ghost">Top 4</span>
          </div>

          <div v-if="leaders" class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-sm" data-testid="game-compare-leaders-grid">
            <div v-if="leaders.topPts" class="border border-base-300 rounded-lg p-3">
              <div class="font-semibold">Top PTS</div>
              <div class="opacity-80">
                {{ leaders.topPts.playerName }} ({{ leaders.topPts.teamAbbr }})
              </div>
              <div class="text-lg font-bold mt-1">{{ leaders.topPts.projPts.toFixed(1) }}</div>
            </div>

            <div v-if="leaders.topPra" class="border border-base-300 rounded-lg p-3">
              <div class="font-semibold">Top PRA</div>
              <div class="opacity-80">
                {{ leaders.topPra.playerName }} ({{ leaders.topPra.teamAbbr }})
              </div>
              <div class="text-lg font-bold mt-1">{{ leaders.topPra.projPra.toFixed(1) }}</div>
            </div>

            <div v-if="leaders.topReb" class="border border-base-300 rounded-lg p-3">
              <div class="font-semibold">Top REB</div>
              <div class="opacity-80">
                {{ leaders.topReb.playerName }} ({{ leaders.topReb.teamAbbr }})
              </div>
              <div class="text-lg font-bold mt-1">{{ leaders.topReb.projReb.toFixed(1) }}</div>
            </div>

            <div v-if="leaders.topAst" class="border border-base-300 rounded-lg p-3">
              <div class="font-semibold">Top AST</div>
              <div class="opacity-80">
                {{ leaders.topAst.playerName }} ({{ leaders.topAst.teamAbbr }})
              </div>
              <div class="text-lg font-bold mt-1">{{ leaders.topAst.projAst.toFixed(1) }}</div>
            </div>
          </div>

          <div v-else class="opacity-70" data-testid="game-compare-no-leaders">
            No leader projections available.
          </div>
        </div>
      </div>

      <!-- Tables -->
      <div class="space-y-4" data-testid="game-compare-home-card">
        <div class="card bg-base-100 shadow">
          <div class="card-body p-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="card-title text-base">{{ home }} players vs {{ away }} defense</h3>
              <span class="badge badge-ghost" data-testid="game-compare-home-count">{{ players.homeRows.length }}</span>
            </div>
            <div data-testid="game-compare-home-table">
              <PlayerTable :title="`${home} players vs ${away} defense`" :rows="players.homeRows" />
            </div>
          </div>
        </div>

        <div class="card bg-base-100 shadow" data-testid="game-compare-away-card">
          <div class="card-body p-4">
            <div class="flex items-center justify-between mb-2">
              <h3 class="card-title text-base">{{ away }} players vs {{ home }} defense</h3>
              <span class="badge badge-ghost" data-testid="game-compare-away-count">{{ players.awayRows.length }}</span>
            </div>
            <div data-testid="game-compare-away-table">
              <PlayerTable :title="`${away} players vs ${home} defense`" :rows="players.awayRows" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
