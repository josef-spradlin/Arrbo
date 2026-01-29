export type GameDto = {
  gameId: string
  gameDate: string // "YYYY-MM-DD"
  startTimeUtc?: string | null
  statusText?: string | null

  homeTeamId?: number | null
  homeTeamAbbr: string
  homeTeamScore?: number | null

  awayTeamId?: number | null
  awayTeamAbbr: string
  awayTeamScore?: number | null
}

// /api/usage/top
export type UsageTopRawDto = {
  teamId: number
  player1Name: string
  player1Usage: number // 0..1
  player2Name: string
  player2Usage: number // 0..1
}

// Normalized: what our app uses
export type UsagePlayerDto = {
  teamId: number
  teamAbbr: string
  playerName: string
  usagePct: number // 0..100
}

// /api/averages
export type PlayerAverageRawDto = {
  id: number
  playerName: string
  playerPts: number
  playerReb: number
  playerAst: number
  playerPra: number
}

// Normalized
export type PlayerAverageDto = {
  teamAbbr?: string
  playerName: string
  pts: number
  reb: number
  ast: number
  pra: number
}

// /api/positions
export type PlayerPositionRawDto = {
  id: number
  playerName: string
  playerPosition: string // "G", "F", "C", "F-C", "G-F", etc.
}

// Normalized 
export type PlayerPositionDto = {
  playerName: string
  position: 'PG' | 'SG' | 'SF' | 'PF' | 'C' | string
}

// /api/defense/efficiency
export type DefensiveEfficiencyRawDto = {
  teamId: number
  pgEfficiency: number
  sgEfficiency: number
  sfEfficiency: number
  pfEfficiency: number
  cefficiency: number
}

// Normalized (one row per team+position)
export type DefensiveEfficiencyDto = {
  teamAbbr: string
  position: 'PG' | 'SG' | 'SF' | 'PF' | 'C' | string
  defEff: number
}

// Enriched computed types
export type EnrichedPlayer = {
  teamAbbr: string
  opponentAbbr: string
  playerName: string
  usagePct: number
  position?: string
  pts: number
  reb: number
  ast: number
  pra: number
  projPts: number
  projReb: number
  projAst: number
  projPra: number
}

export type MatchupLeaders = {
  topPts?: EnrichedPlayer
  topReb?: EnrichedPlayer
  topAst?: EnrichedPlayer
  topPra?: EnrichedPlayer
  bottomPts?: EnrichedPlayer
  bottomReb?: EnrichedPlayer
  bottomAst?: EnrichedPlayer
  bottomPra?: EnrichedPlayer
}