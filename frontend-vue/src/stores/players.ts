/**
 * Players store
 *
 * Responsible for:
 * - Loading player usage, averages, positions, and defensive efficiency
 * - Building matchup-specific player projections
 * - Applying usage, defensive efficiency, and home/away adjustments
 *
 * This is where the core projection logic for the model lives.
 */

import { defineStore } from 'pinia'
import type {
  DefensiveEfficiencyDto,
  EnrichedPlayer,
  GameDto,
  MatchupLeaders,
  PlayerAverageDto,
  PlayerPositionDto,
  UsagePlayerDto,
} from '@/types/dto'
import {
  getAverages,
  getDefensiveEfficiency,
  getPositions,
  getTopUsagePlayers,
} from '@/api/arrbo'

type State = {
  usagePlayers: UsagePlayerDto[]
  averages: PlayerAverageDto[]
  positions: PlayerPositionDto[]
  defense: DefensiveEfficiencyDto[]
  loading: boolean
  error: string | null

  selectedGame: GameDto | null
  matchupPlayers: EnrichedPlayer[]
  leaders: MatchupLeaders | null
}

function normTeam(s: string | null | undefined) {
  return (s ?? '').trim().toUpperCase()
}

export const usePlayersStore = defineStore('players', {
  state: (): State => ({
    usagePlayers: [],
    averages: [],
    positions: [],
    defense: [],
    loading: false,
    error: null,

    selectedGame: null,
    matchupPlayers: [],
    leaders: null,
  }),

  getters: {
    homeRows: (state) => {
      const home = normTeam(state.selectedGame?.homeTeamAbbr)
      return home ? state.matchupPlayers.filter((p) => normTeam(p.teamAbbr) === home) : []
    },
    awayRows: (state) => {
      const away = normTeam(state.selectedGame?.awayTeamAbbr)
      return away ? state.matchupPlayers.filter((p) => normTeam(p.teamAbbr) === away) : []
    },
  },

  actions: {
    async ensureDataLoaded() {
      const [usagePlayers, averages, positions, defense] = await Promise.all([
        getTopUsagePlayers(),
        getAverages(),
        getPositions(),
        getDefensiveEfficiency(),
      ])

      this.usagePlayers = usagePlayers
      this.averages = averages
      this.positions = positions
      this.defense = defense
    },

    async loadMatchup(home: string, away: string, date?: string) {
      const d = date ?? new Date().toISOString().slice(0, 10)

      const game: GameDto = {
        gameId: `${away}@${home}:${d}`,
        gameDate: d,
        homeTeamAbbr: home,
        awayTeamAbbr: away,
      }

      await this.selectGame(game)
    },

    projectPlayersForGame(game: GameDto): EnrichedPlayer[] {
      const homeAbbr = normTeam(game.homeTeamAbbr)
      const awayAbbr = normTeam(game.awayTeamAbbr)

      const flattenTeamTop5 = (teamRow: any) => {
        const teamAbbr = normTeam(teamRow.teamAbbr)
        const pairs = [
          [teamRow.player1Name, teamRow.player1Usage],
          [teamRow.player2Name, teamRow.player2Usage],
          [teamRow.player3Name, teamRow.player3Usage],
          [teamRow.player4Name, teamRow.player4Usage],
          [teamRow.player5Name, teamRow.player5Usage],
        ] as const

        return pairs
          .filter(([name, usage]) => !!name && usage != null)
          .map(([name, usage]) => ({
            teamAbbr,
            playerName: String(name),
            usagePct: Number(usage),
          }))
      }

      const isTeamRowShape =
        this.usagePlayers.length > 0 && (this.usagePlayers[0] as any).player1Name != null

      const usageFlat = isTeamRowShape
        ? (this.usagePlayers as any[])
            .filter((u) => {
              const t = normTeam(u.teamAbbr)
              return t === homeAbbr || t === awayAbbr
            })
            .flatMap(flattenTeamTop5)
        : (this.usagePlayers as any[]).filter((u) => {
            const t = normTeam(u.teamAbbr)
            return t === homeAbbr || t === awayAbbr
          })

      const avgByName = new Map(this.averages.map((a) => [a.playerName, a]))
      const posByName = new Map(this.positions.map((p) => [p.playerName, p.position]))
      const defByTeamPos = new Map(
        this.defense.map((d) => [`${normTeam(d.teamAbbr)}::${d.position}`, d.defEff])
      )

      const enriched: EnrichedPlayer[] = usageFlat.map((u) => {
        const teamAbbr = normTeam(u.teamAbbr)
        const opponentAbbr = teamAbbr === homeAbbr ? awayAbbr : homeAbbr

        const position = posByName.get(u.playerName)
        const avg = avgByName.get(u.playerName) ?? {
          playerName: u.playerName,
          pts: 0,
          reb: 0,
          ast: 0,
          pra: 0,
        }

        const def = position ? defByTeamPos.get(`${opponentAbbr}::${position}`) : undefined

        const usageBoost = 1 + Math.min(Math.max((u.usagePct - 20) / 200, -0.05), 0.08)
      const defAdj = def == null ? 1 : 1 + Math.min(Math.max((100 - def) / 500, -0.08), 0.08)

      // Home/away adjustment (modest and stat-specific)
      const isHome = teamAbbr === homeAbbr

      const HOME_EDGE_PTS = 0.03   // +/- 3.0%
      const HOME_EDGE_REB = 0.015  // +/- 1.5%
      const HOME_EDGE_AST = 0.02   // +/- 2.0%

      const haPts = isHome ? (1 + HOME_EDGE_PTS) : (1 - HOME_EDGE_PTS)
      const haReb = isHome ? (1 + HOME_EDGE_REB) : (1 - HOME_EDGE_REB)
      const haAst = isHome ? (1 + HOME_EDGE_AST) : (1 - HOME_EDGE_AST)

      // Base matchup multiplier (usage + defense) then apply stat-specific home/away factor
      const baseMult = usageBoost * defAdj
      const multPts = baseMult * haPts
      const multReb = baseMult * haReb
      const multAst = baseMult * haAst

      const projPts = +(avg.pts * multPts).toFixed(1)
      const projReb = +(avg.reb * multReb).toFixed(1)
      const projAst = +(avg.ast * multAst).toFixed(1)
      const projPra = +(projPts + projReb + projAst).toFixed(1)


        return {
          teamAbbr,
          opponentAbbr,
          playerName: u.playerName,
          usagePct: u.usagePct,
          position,
          pts: avg.pts,
          reb: avg.reb,
          ast: avg.ast,
          pra: avg.pra,
            projPts,
            projReb,
            projAst,
            projPra,
        }
      })

      return enriched
    },


    buildProjectionsForGame(game: GameDto) {
      const enriched = this.projectPlayersForGame(game)

      const sortDesc = <K extends keyof EnrichedPlayer>(k: K) =>
        [...enriched].sort((a, b) => (b[k] as number) - (a[k] as number))
      const sortAsc = <K extends keyof EnrichedPlayer>(k: K) =>
        [...enriched].sort((a, b) => (a[k] as number) - (b[k] as number))

      this.leaders = enriched.length
        ? {
            topPts: sortDesc('projPts')[0],
            topReb: sortDesc('projReb')[0],
            topAst: sortDesc('projAst')[0],
            topPra: sortDesc('projPra')[0],
            bottomPts: sortAsc('projPts')[0],
            bottomReb: sortAsc('projReb')[0],
            bottomAst: sortAsc('projAst')[0],
            bottomPra: sortAsc('projPra')[0],
          }
        : null

      this.matchupPlayers = enriched
    },

    async selectGame(game: GameDto) {
      try {
        this.loading = true
        this.error = null
        this.selectedGame = game

        await this.ensureDataLoaded()
        this.buildProjectionsForGame(game)
      } catch (e: any) {
        this.error = e?.message ?? 'Failed to build matchup predictions'
        this.matchupPlayers = []
        this.leaders = null
      } finally {
        this.loading = false
      }
    },
  },
})
