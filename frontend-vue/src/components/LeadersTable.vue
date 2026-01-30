<script setup lang="ts">
import type { EnrichedPlayer } from '@/types/dto'

const props = defineProps<{
  rows: EnrichedPlayer[]
  stat: 'projPts' | 'projReb' | 'projAst' | 'projPra'
}>()
</script>

<template>
  <div class="overflow-x-auto">
    <table class="w-full text-sm">
      <thead class="border-b">
        <tr>
          <th class="text-left p-2 w-10">#</th>
          <th class="text-left p-2">Player</th>
          <th class="text-left p-2 w-20">Team</th>
          <th class="text-left p-2 w-20">Opp</th>
          <th class="text-right p-2 w-20">Proj</th>
        </tr>
      </thead>

      <tbody>
        <tr
          v-for="(p, i) in props.rows"
          :key="p.teamAbbr + p.playerName + i"
          class="border-b last:border-b-0"
        >
          <td class="p-2">{{ i + 1 }}</td>
          <td class="p-2">{{ p.playerName }}</td>
          <td class="p-2">{{ p.teamAbbr }}</td>
          <td class="p-2">{{ p.opponentAbbr }}</td>
          <td class="p-2 text-right">{{ Number(p[props.stat]).toFixed(1) }}</td>
        </tr>

        <tr v-if="props.rows.length === 0">
          <td colspan="5" class="p-3 text-center opacity-70">
            No players found for this day.
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>
