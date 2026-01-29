import { defineStore } from 'pinia'
import type { GameDto } from '@/types/dto'
import { getGames } from '@/api/arrbo'

type State = {
  gamesByDate: Record<string, GameDto[]>
  loading: boolean
  error: string | null
}

export const useGamesStore = defineStore('games', {
  state: (): State => ({
    gamesByDate: {},
    loading: false,
    error: null,
  }),

  actions: {
    async load(date: string) {
      try {
        this.loading = true
        this.error = null
        this.gamesByDate[date] = await getGames(date)
      } catch (e: any) {
        this.error = e?.message ?? 'Failed to load games'
      } finally {
        this.loading = false
      }
    },
  },
})
