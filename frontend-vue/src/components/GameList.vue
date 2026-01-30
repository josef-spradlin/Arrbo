<script setup lang="ts">
import type { GameDto } from '@/types/dto'
import { teamColor} from '@/utils/teamColors'

const props = defineProps({
  games: {
    type: Array as () => GameDto[],
    default: () => [],
  },
  selectedGameId: {
    type: String,
    default: '',
  },
})


const emit = defineEmits<{
  (e: 'select', game: GameDto): void
}>()

function statusBadgeClass(status?: string | null) {
  const s = (status ?? '').toLowerCase()
  if (!s) return 'badge-ghost'
  if (s.includes('final')) return 'badge-success'
  if (s.includes('live') || s.includes('in progress')) return 'badge-warning'
  if (s.includes('scheduled') || s.includes('pre')) return 'badge-info'
  return 'badge-ghost'
}

</script>

<template>
  <div>
    <div v-if="props.games.length === 0" class="opacity-70 text-sm">
      No games
    </div>

    <ul v-else class="menu p-0">
      <li v-for="g in props.games" :key="g.gameId">
        <button class="flex items-center justify-between gap-3 py-3 px-3 rounded-lg transition hover:bg-base-300":class="g.gameId === props.selectedGameId? 'bg-base-200 ring-2 ring-primary/40 opacity-100': 'bg-base-100 opacity-70'"@click="emit('select', g)"type="button">
          <div class="font-medium" :class="g.gameId === props.selectedGameId ? 'font-semibold' : ''">
            <span :style="{ color: teamColor(g.awayTeamAbbr) }">
              {{ g.awayTeamAbbr }}
            </span>
            <span class="opacity-60 mx-1">@</span>
            <span :style="{ color: teamColor(g.homeTeamAbbr) }">
              {{ g.homeTeamAbbr }}
            </span>
          </div>

          <span class="badge" :class="statusBadgeClass(g.statusText)">
            {{ g.statusText ?? '—' }}
          </span>
        </button>
      </li>
    </ul>
  </div>
</template>
