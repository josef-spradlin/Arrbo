<script setup lang="ts">
import type { GameDto, MatchupLeaders } from '@/types/dto'

defineProps<{
  game: GameDto
  leaders: MatchupLeaders | null
  loading: boolean
  error: string | null
}>()
</script>

<template>
  <div style="border:1px solid #ddd; padding: 12px;">
    <div style="font-weight: 700;">
      {{ game.awayTeamAbbr }} @ {{ game.homeTeamAbbr }} — {{ game.gameDate }}
    </div>

    <div v-if="loading" style="margin-top: 10px;">Loading predictions…</div>
    <div v-else-if="error" style="margin-top: 10px; color:red;">{{ error }}</div>
    <div v-else-if="!leaders" style="margin-top: 10px;">No prediction data.</div>

    <div v-else style="margin-top: 10px;">
      <div><b>Top PTS:</b> {{ leaders.topPts?.playerName }} ({{ leaders.topPts?.projPts }})</div>
      <div><b>Top REB:</b> {{ leaders.topReb?.playerName }} ({{ leaders.topReb?.projReb }})</div>
      <div><b>Top AST:</b> {{ leaders.topAst?.playerName }} ({{ leaders.topAst?.projAst }})</div>
      <div><b>Top PRA:</b> {{ leaders.topPra?.playerName }} ({{ leaders.topPra?.projPra }})</div>

      <hr style="margin: 10px 0;" />

      <div><b>Lowest PTS:</b> {{ leaders.bottomPts?.playerName }} ({{ leaders.bottomPts?.projPts }})</div>
      <div><b>Lowest REB:</b> {{ leaders.bottomReb?.playerName }} ({{ leaders.bottomReb?.projReb }})</div>
      <div><b>Lowest AST:</b> {{ leaders.bottomAst?.playerName }} ({{ leaders.bottomAst?.projAst }})</div>
      <div><b>Lowest PRA:</b> {{ leaders.bottomPra?.playerName }} ({{ leaders.bottomPra?.projPra }})</div>
    </div>
  </div>
</template>
