import { http } from './http'
import type {
  GameDto,
  UsagePlayerDto,
  UsageTopRawDto,
  PlayerAverageDto,
  PlayerAverageRawDto,
  PlayerPositionDto,
  PlayerPositionRawDto,
  DefensiveEfficiencyDto,
  DefensiveEfficiencyRawDto,
} from '@/types/dto'

const TEAM_ID_TO_ABBR: Record<number, string> = {
  1: 'ATL', 2: 'BOS', 3: 'BKN', 4: 'CHA', 5: 'CHI', 6: 'CLE', 7: 'DAL', 8: 'DEN',
  9: 'DET', 10: 'GSW', 11: 'HOU', 12: 'IND', 13: 'LAC', 14: 'LAL', 15: 'MEM',
  16: 'MIA', 17: 'MIL', 18: 'MIN', 19: 'NOP', 20: 'NYK', 21: 'OKC', 22: 'ORL',
  23: 'PHI', 24: 'PHX', 25: 'POR', 26: 'SAC', 27: 'SAS', 28: 'TOR', 29: 'UTA',
  30: 'WAS',
}

function toAbbr(teamId: number) {
  return TEAM_ID_TO_ABBR[teamId] ?? ''
}

function clampUsagePct(x: number) {
  return +(x * 100).toFixed(1)
}

function mapPosition(posRaw: string): PlayerPositionDto['position'] {
  const p = (posRaw ?? '').trim().toUpperCase()

  //Map combo positions to primary
  if (p === 'C') return 'C'
  if (p === 'G') return 'PG'
  if (p === 'F') return 'SF'

  if (p.includes('C')) return 'C'
  if (p.includes('G')) return 'PG'
  if (p.includes('F')) return 'SF'

  return p || 'SF'
}

export async function getGames(date: string) {
  const { data } = await http.get<GameDto[]>('/api/games', { params: { date } })
  return data
}

export async function getTopUsagePlayers() {
  const { data } = await http.get<UsageTopRawDto[]>('/api/usage/top')

  const flat: UsagePlayerDto[] = data.flatMap((row) => {
    const teamAbbr = toAbbr(row.teamId)
    if (!teamAbbr) return []

    return [
      {
        teamId: row.teamId,
        teamAbbr,
        playerName: row.player1Name,
        usagePct: clampUsagePct(row.player1Usage),
      },
      {
        teamId: row.teamId,
        teamAbbr,
        playerName: row.player2Name,
        usagePct: clampUsagePct(row.player2Usage),
      },
      {
        teamId: row.teamId,
        teamAbbr,
        playerName: row.player3Name,
        usagePct: clampUsagePct(row.player3Usage),
      },
      {
        teamId: row.teamId,
        teamAbbr,
        playerName: row.player4Name,
        usagePct: clampUsagePct(row.player4Usage),
      },
      {
        teamId: row.teamId,
        teamAbbr,
        playerName: row.player5Name,
        usagePct: clampUsagePct(row.player5Usage),
      },
    ].filter((p) => !!p.playerName)
  })

  return flat
}


export async function getAverages() {
  const { data } = await http.get<PlayerAverageRawDto[]>('/api/averages')

  const normalized: PlayerAverageDto[] = data.map((r) => ({
    playerName: r.playerName,
    pts: r.playerPts,
    reb: r.playerReb,
    ast: r.playerAst,
    pra: r.playerPra,
  }))

  return normalized
}

export async function getPositions() {
  const { data } = await http.get<PlayerPositionRawDto[]>('/api/positions')

  const normalized: PlayerPositionDto[] = data.map((r) => ({
    playerName: r.playerName,
    position: mapPosition(r.playerPosition),
  }))

  return normalized
}

export async function getDefensiveEfficiency() {
  const { data } = await http.get<DefensiveEfficiencyRawDto[]>('/api/defense/efficiency')

  const normalized: DefensiveEfficiencyDto[] = data.flatMap((r) => {
    const teamAbbr = toAbbr(r.teamId)
    if (!teamAbbr) return []

    return [
      { teamAbbr, position: 'PG', defEff: r.pgEfficiency },
      { teamAbbr, position: 'SG', defEff: r.sgEfficiency },
      { teamAbbr, position: 'SF', defEff: r.sfEfficiency },
      { teamAbbr, position: 'PF', defEff: r.pfEfficiency },
      { teamAbbr, position: 'C', defEff: r.cefficiency },
    ]
  })

  return normalized
}
