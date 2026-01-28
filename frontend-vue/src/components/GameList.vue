<template>
  <div v-if="!games.length" style="opacity: 0.7;">No games found.</div>

  <div v-for="g in games" :key="g.gameId"
       @click="go(g.gameId)"
       style="border: 1px solid #ddd; border-radius: 10px; padding: 10px; margin-bottom: 10px; cursor: pointer;">
    <div style="display:flex; justify-content: space-between; gap: 12px;">
      <div>
        <div style="font-weight: 600;">
          {{ g.awayTeamAbbr }} @ {{ g.homeTeamAbbr }}
        </div>
        <div style="font-size: 12px; opacity: 0.8;">
          {{ g.statusText }} <span v-if="timeText(g)">• {{ timeText(g) }}</span>
        </div>
      </div>

      <div style="text-align:right;">
        <div v-if="g.homeScore != null && g.awayScore != null" style="font-weight: 600;">
          {{ g.awayScore }} - {{ g.homeScore }}
        </div>
        <div v-else style="font-size: 12px; opacity: 0.7;">
          —
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { GameDto } from '../types/dto'

const props = defineProps<{ games: GameDto[] }>()
const router = useRouter()

function go(gameId: string) {
  router.push(`/compare/${gameId}`)
}

function timeText(g: GameDto): string | null {
  if (!g.startTimeUtc) return null
  // Display in user's local time
  const d = new Date(g.startTimeUtc)
  return d.toLocaleTimeString([], { hour: 'numeric', minute: '2-digit' })
}
</script>
