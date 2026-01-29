<script setup lang="ts">
import type { GameDto } from '@/types/dto'

defineProps<{
  games: GameDto[]
}>()

const emit = defineEmits<{
  (e: 'select', game: GameDto): void
}>()
</script>

<template>
  <div>
    <div v-if="games.length === 0" style="opacity: 0.7;">No games</div>

    <button
      v-for="g in games"
      :key="g.gameId"
      @click="emit('select', g)"
      style="display:block; width:100%; text-align:left; margin:6px 0; padding:10px;"
    >
      {{ g.awayTeamAbbr }} @ {{ g.homeTeamAbbr }}
      <span style="float:right; opacity:0.7;">{{ g.statusText }}</span>
    </button>
  </div>
</template>
