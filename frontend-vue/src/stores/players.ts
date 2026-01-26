// src/stores/players.ts
import { defineStore } from 'pinia'
import type { TopUsagePlayerDto } from '../types/dto'
import { getTopUsagePlayers } from '../api/arrbo'

type PlayersState = {
  topUsage: TopUsagePlayerDto[]
  loadingTopUsage: boolean
  topUsageError: string | null
}

export const usePlayersStore = defineStore('players', {
  state: (): PlayersState => ({
    topUsage: [],
    loadingTopUsage: false,
    topUsageError: null,
  }),

  getters: {
    topUsageByTeam: (state) => {
      const map = new Map<number, TopUsagePlayerDto[]>()
      for (const p of state.topUsage) {
        const arr = map.get(p.teamId) ?? []
        arr.push(p)
        map.set(p.teamId, arr)
      }
      return map
    },
  },

  actions: {
    async fetchTopUsage(opts?: { force?: boolean }) {
      const force = opts?.force ?? false
      if (!force && this.topUsage.length) return

      this.loadingTopUsage = true
      this.topUsageError = null
      try {
        this.topUsage = await getTopUsagePlayers()
      } catch (e: any) {
        this.topUsageError = e?.message ?? 'Failed to load top usage players'
      } finally {
        this.loadingTopUsage = false
      }
    },
  },
})
