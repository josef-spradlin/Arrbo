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
  <div>
    <h1>Game Compare</h1>
    <div>Game ID: {{ gameId }} | {{ away }} @ {{ home }} | Date: {{ date }}</div>

    <div v-if="players.loading">Loading matchup data...</div>
    <div v-else-if="players.error">{{ players.error }}</div>

    <div v-else>
      <h2>Predicted Leaders</h2>

      <ul v-if="leaders">
        <li v-if="leaders.topPts">
          Top PTS: {{ leaders.topPts.playerName }} ({{ leaders.topPts.teamAbbr }}) —
          {{ leaders.topPts.projPts.toFixed(1) }}
        </li>

        <li v-if="leaders.topAst">
          Top AST: {{ leaders.topAst.playerName }} ({{ leaders.topAst.teamAbbr }}) —
          {{ leaders.topAst.projAst.toFixed(1) }}
        </li>

        <li v-if="leaders.topReb">
          Top REB: {{ leaders.topReb.playerName }} ({{ leaders.topReb.teamAbbr }}) —
          {{ leaders.topReb.projReb.toFixed(1) }}
        </li>

        <li v-if="leaders.topPra">
          Top PRA: {{ leaders.topPra.playerName }} ({{ leaders.topPra.teamAbbr }}) —
          {{ leaders.topPra.projPra.toFixed(1) }}
        </li>
      </ul>

      <div v-else style="opacity: 0.7;">No leader projections available.</div>

      <PlayerTable :title="`${home} players vs ${away} defense`" :rows="players.homeRows" />
      <br />
      <PlayerTable :title="`${away} players vs ${home} defense`" :rows="players.awayRows" />
    </div>
  </div>
</template>
