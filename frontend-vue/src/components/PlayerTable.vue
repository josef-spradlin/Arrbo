<script setup lang="ts">
import type { EnrichedPlayer } from '@/types/dto'

defineProps<{
  title?: string
  rows: EnrichedPlayer[]
}>()
</script>

<template>
  <div>
    <h3 v-if="title">{{ title }}</h3>

    <table border="1" cellpadding="6" cellspacing="0" style="width:100%; border-collapse: collapse;">
      <thead>
        <tr>
          <th>Team</th>
          <th>Opp</th>
          <th>Player</th>
          <th>Pos</th>
          <th>Usage%</th>
          <th>PTS</th><th>REB</th><th>AST</th><th>PRA</th>
          <th>Proj PTS</th><th>Proj REB</th><th>Proj AST</th><th>Proj PRA</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="p in rows" :key="p.teamAbbr + '::' + p.playerName">
          <td>{{ p.teamAbbr }}</td>
          <td>{{ p.opponentAbbr }}</td>
          <td>{{ p.playerName }}</td>
          <td>{{ p.position ?? '-' }}</td>
          <td>{{ p.usagePct.toFixed(1) }}</td>
          <td>{{ p.pts.toFixed(1) }}</td>
          <td>{{ p.reb.toFixed(1) }}</td>
          <td>{{ p.ast.toFixed(1) }}</td>
          <td>{{ p.pra.toFixed(1) }}</td>
          <td>{{ p.projPts.toFixed(1) }}</td>
          <td>{{ p.projReb.toFixed(1) }}</td>
          <td>{{ p.projAst.toFixed(1) }}</td>
          <td>{{ p.projPra.toFixed(1) }}</td>
        </tr>
      </tbody>
    </table>

    <div v-if="rows.length === 0" style="margin-top: 8px; opacity: 0.7;">
      No players loaded for this matchup.
    </div>
  </div>
</template>
