<script setup lang="ts">
import type { EnrichedPlayer } from '@/types/dto'
import { teamColor } from '@/utils/teamColors'


const props = defineProps<{
  rows: EnrichedPlayer[]
  stat: 'projPts' | 'projReb' | 'projAst' | 'projPra'
}>()

function baseStat(p: EnrichedPlayer) {
  switch (props.stat) {
    case 'projPts':
      return p.pts
    case 'projReb':
      return p.reb
    case 'projAst':
      return p.ast
    case 'projPra':
      return p.pra
  }
}

</script>

<template>
  <div class="overflow-x-auto">
    <table class="table table-zebra w-full text-sm">
      <thead>
        <tr>
          <th class="w-12">#</th>
          <th>Player</th>
          <th class="w-20">Team</th>
          <th class="w-20">Opp</th>
          <th class="w-20 text-right">Current Avg</th>
          <th class="w-24 text-right">Proj</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="(p, i) in props.rows" :key="p.teamAbbr + p.playerName + i">
          <td>{{ i + 1 }}</td>
          <td class="font-medium">{{ p.playerName }}</td>
          <td class="p-2">
            <div class="flex items-center gap-2">
                <span class="inline-block h-2.5 w-2.5 rounded-full" :style="{ backgroundColor: teamColor(p.teamAbbr) }"/>
                <span class="font-semibold">{{ p.teamAbbr }}</span>
            </div>
            </td>
            <td class="p-2">
            <div class="flex items-center gap-2">
                <span class="inline-block h-2.5 w-2.5 rounded-full opacity-70" :style="{ backgroundColor: teamColor(p.opponentAbbr) }"/>
                <span>{{ p.opponentAbbr }}</span>
            </div>
            </td>
          <td class="text-right opacity-70">
            {{ baseStat(p).toFixed(1) }}
            </td>

            <td class="text-right font-semibold">
            {{ Number(p[props.stat]).toFixed(1) }}
            </td>
        </tr>

        <tr v-if="props.rows.length === 0">
          <td colspan="6" class="text-center opacity-70 py-6">
            No players found.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
