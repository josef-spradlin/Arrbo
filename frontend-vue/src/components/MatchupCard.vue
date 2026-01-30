<script setup lang="ts">
import type { GameDto, MatchupLeaders } from '@/types/dto'
import { teamColor } from '@/utils/teamColors'

defineProps<{
  game: GameDto
  leaders: MatchupLeaders | null
  loading: boolean
  error: string | null
}>()
</script>

<template>
  <div class="space-y-3">
    <div class="flex items-center justify-between gap-2">
      <div class="font-semibold">
        {{ game.awayTeamAbbr }} <span class="opacity-60">@</span> {{ game.homeTeamAbbr }}
      </div>
      <span class="badge badge-ghost">{{ game.gameDate }}</span>
    </div>

    <div v-if="loading" class="alert">
      <span>Loading predictions…</span>
    </div>

    <div v-else-if="error" class="alert alert-error">
      <span>{{ error }}</span>
    </div>

    <div v-else-if="!leaders" class="alert alert-warning">
      <span>No prediction data.</span>
    </div>

    <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-3">
      <!-- Top -->
      <div class="card bg-base-200">
        <div class="card-body p-4">
          <div class="font-semibold mb-2">Top Projections</div>

          <div class="stats stats-vertical bg-base-100 shadow">
            <div class="stat py-3">
              <div class="stat-title">PTS</div>
              <div class="stat-value text-lg">{{ leaders.topPts?.projPts?.toFixed?.(1) }}</div>
              <div class="stat-desc">
                <span
                  class="inline-block h-2.5 w-2.5 rounded-full mr-2 align-middle"
                  :style="{ backgroundColor: teamColor(leaders.topPts?.teamAbbr) }"
                />
                <span class="font-semibold">{{ leaders.topPts?.playerName }}</span>
                <span class="opacity-70"> ({{ leaders.topPts?.teamAbbr }})</span>
              </div>
            </div>

            <div class="stat py-3">
              <div class="stat-title">REB</div>
              <div class="stat-value text-lg">{{ leaders.topReb?.projReb?.toFixed?.(1) }}</div>
              <div class="stat-desc">
                <span class="inline-block h-2.5 w-2.5 rounded-full mr-2 align-middle" :style="{ backgroundColor: teamColor(leaders.topReb?.teamAbbr) }"/>
                <span class="font-semibold">{{ leaders.topReb?.playerName }}</span>
                <span class="opacity-70"> ({{ leaders.topReb?.teamAbbr }})</span>
              </div>
            </div>
            <div class="stat py-3">
              <div class="stat-title">AST</div>
              <div class="stat-value text-lg">{{ leaders.topAst?.projAst?.toFixed?.(1) }}</div>
              <div class="stat-desc">
                <span class="inline-block h-2.5 w-2.5 rounded-full mr-2 align-middle" :style="{ backgroundColor: teamColor(leaders.topAst?.teamAbbr) }"/>
                <span class="font-semibold">{{ leaders.topAst?.playerName }}</span>
                <span class="opacity-70"> ({{ leaders.topAst?.teamAbbr }})</span>
              </div>
            </div>

            <div class="stat py-3">
              <div class="stat-title">PRA</div>
              <div class="stat-value text-lg">{{ leaders.topPra?.projPra?.toFixed?.(1) }}</div>
              <div class="stat-desc">
                <span class="inline-block h-2.5 w-2.5 rounded-full mr-2 align-middle" :style="{ backgroundColor: teamColor(leaders.topPra?.teamAbbr) }"/>
                <span class="font-semibold">{{ leaders.topPra?.playerName }}</span>
                <span class="opacity-70"> ({{ leaders.topPra?.teamAbbr }})</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Bottom -->
      <div class="card bg-base-200">
        <div class="card-body p-4">
          <div class="font-semibold mb-2">Lowest Projections</div>

          <div class="stats stats-vertical bg-base-100 shadow">
            <div class="stat py-3">
              <div class="stat-title">PTS</div>
              <div class="stat-value text-lg">{{ leaders.bottomPts?.projPts?.toFixed?.(1) }}</div>
              <div class="stat-desc">
                <span class="inline-block h-2.5 w-2.5 rounded-full mr-2 align-middle" :style="{ backgroundColor: teamColor(leaders.bottomPts?.teamAbbr) }"/>
                <span class="font-semibold">{{ leaders.bottomPts?.playerName }}</span>
                <span class="opacity-70"> ({{ leaders.bottomPts?.teamAbbr }})</span>
              </div>
            </div>

            <div class="stat py-3">
              <div class="stat-title">REB</div>
              <div class="stat-value text-lg">{{ leaders.bottomReb?.projReb?.toFixed?.(1) }}</div>
              <div class="stat-desc">
                <span class="inline-block h-2.5 w-2.5 rounded-full mr-2 align-middle" :style="{ backgroundColor: teamColor(leaders.bottomReb?.teamAbbr) }"/>
                <span class="font-semibold">{{ leaders.bottomReb?.playerName }}</span>
                <span class="opacity-70"> ({{ leaders.bottomReb?.teamAbbr }})</span>
              </div>
            </div>
            <div class="stat py-3">
              <div class="stat-title">AST</div>
              <div class="stat-value text-lg">{{ leaders.bottomAst?.projAst?.toFixed?.(1) }}</div>
              <div class="stat-desc">
                <span class="inline-block h-2.5 w-2.5 rounded-full mr-2 align-middle":style="{ backgroundColor: teamColor(leaders.bottomAst?.teamAbbr) }"/>
                <span class="font-semibold">{{ leaders.bottomAst?.playerName }}</span>
                <span class="opacity-70"> ({{ leaders.bottomAst?.teamAbbr }})</span>
              </div>
            </div>

            <div class="stat py-3">
              <div class="stat-title">PRA</div>
              <div class="stat-value text-lg">{{ leaders.bottomPra?.projPra?.toFixed?.(1) }}</div>
              <div class="stat-desc">
                <span class="inline-block h-2.5 w-2.5 rounded-full mr-2 align-middle" :style="{ backgroundColor: teamColor(leaders.bottomPra?.teamAbbr) }"/>
                <span class="font-semibold">{{ leaders.bottomPra?.playerName }}</span>
                <span class="opacity-70"> ({{ leaders.bottomPra?.teamAbbr }})</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
