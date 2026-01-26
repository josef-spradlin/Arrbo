// src/stores/games.ts
import { defineStore } from 'pinia'
import type { GameDto, ISODate } from '../types/dto'
import { getGamesByDate } from '../api/arrbo'

type GamesState = {
  byDate: Record<ISODate, GameDto[]>
  loadingByDate: Record<ISODate, boolean>
  errorByDate: Record<ISODate, string | null>
}

export const useGamesStore = defineStore('games', {
  state: (): GamesState => ({
    byDate: {},
    loadingByDate: {},
    errorByDate: {},
  }),

  getters: {
    gamesForDate: (state) => (date: ISODate) => state.byDate[date] ?? [],
    isLoading: (state) => (date: ISODate) => state.loadingByDate[date] ?? false,
    error: (state) => (date: ISODate) => state.errorByDate[date] ?? null,
  },

  actions: {
    async fetchGames(date: ISODate, opts?: { force?: boolean }) {
      const force = opts?.force ?? false
      if (!force && this.byDate[date]?.length) return

      this.loadingByDate[date] = true
      this.errorByDate[date] = null

      try {
        this.byDate[date] = await getGamesByDate(date)
      } catch (e: any) {
        this.errorByDate[date] = e?.message ?? 'Failed to load games'
      } finally {
        this.loadingByDate[date] = false
      }
    },
  },
})
