<script setup lang="ts">
import type { EnrichedPlayer } from '@/types/dto'

defineProps<{
  title?: string
  rows: EnrichedPlayer[]
}>()

const TEAM_COLORS: Record<string, string> = {
  ATL: '#E03A3E',
  BOS: '#007A33',
  BKN: '#111111',
  CHA: '#1D1160',
  CHI: '#CE1141',
  CLE: '#6F263D',
  DAL: '#00538C',
  DEN: '#0E2240',
  DET: '#C8102E',
  GSW: '#1D428A',
  HOU: '#CE1141',
  IND: '#002D62',
  LAC: '#C8102E',
  LAL: '#552583',
  MEM: '#5D76A9',
  MIA: '#98002E',
  MIL: '#00471B',
  MIN: '#0C2340',
  NOP: '#0C2340',
  NYK: '#006BB6',
  OKC: '#007AC1',
  ORL: '#0077C0',
  PHI: '#006BB6',
  PHX: '#1D1160',
  POR: '#E03A3E',
  SAC: '#5A2D81',
  SAS: '#C4CED4',
  TOR: '#CE1141',
  UTA: '#002B5C',
  WAS: '#002B5C',
}

function teamColor(abbr?: string) {
  const key = (abbr ?? '').toUpperCase()
  return TEAM_COLORS[key] ?? '#94A3B8' // fallback gray
}

</script>

<template>
  <div class="space-y-2">
    <div v-if="title" class="flex items-center justify-between">
      <h3 class="font-semibold">{{ title }}</h3>
      <span class="badge badge-outline">{{ rows.length }}</span>
    </div>

    <div class="overflow-x-auto border border-base-300 rounded-xl">
      <table class="table table-zebra w-full text-sm">
        <thead>
          <tr>
            <th>Team</th>
            <th>Player</th>
            <th>Pos</th>
            <th class="text-right">Usage%</th>
            <th class="text-right">PTS</th>
            <th class="text-right">REB</th>
            <th class="text-right">AST</th>
            <th class="text-right">PRA</th>
            <th class="text-right">Proj PTS</th>
            <th class="text-right">Proj REB</th>
            <th class="text-right">Proj AST</th>
            <th class="text-right">Proj PRA</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="p in rows" :key="p.teamAbbr + '::' + p.playerName">
            <td>
              <div class="flex items-center gap-2">
                <span
                  class="inline-block h-2.5 w-2.5 rounded-full"
                  :style="{ backgroundColor: teamColor(p.teamAbbr) }"
                ></span>
                <span class="font-semibold">{{ p.teamAbbr }}</span>
              </div>
            </td>
            <td class="font-medium">{{ p.playerName }}</td>
            <td>{{ p.position ?? '-' }}</td>
            <td class="text-right">{{ p.usagePct.toFixed(1) }}</td>
            <td class="text-right">{{ p.pts.toFixed(1) }}</td>
            <td class="text-right">{{ p.reb.toFixed(1) }}</td>
            <td class="text-right">{{ p.ast.toFixed(1) }}</td>
            <td class="text-right">{{ p.pra.toFixed(1) }}</td>
            <td class="text-right font-semibold">{{ p.projPts.toFixed(1) }}</td>
            <td class="text-right font-semibold">{{ p.projReb.toFixed(1) }}</td>
            <td class="text-right font-semibold">{{ p.projAst.toFixed(1) }}</td>
            <td class="text-right font-semibold">{{ p.projPra.toFixed(1) }}</td>
          </tr>

          <tr v-if="rows.length === 0">
            <td colspan="13" class="text-center opacity-70 py-6">
              No players loaded for this matchup.
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
