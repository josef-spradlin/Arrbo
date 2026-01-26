// src/types/dto.ts

export type ISODate = string // "YYYY-MM-DD"
export type ISODateTime = string // "2026-01-26T00:30:00Z"

// Games endpoint DTO
export interface GameDto {
  gameId: string
  gameDate: ISODate
  startTimeUtc: ISODateTime | null
  statusText: string

  homeTeamId: number
  homeTeamAbbr: string
  homeScore: number | null

  awayTeamId: number
  awayTeamAbbr: string
  awayScore: number | null
}

// Usage endpoint DTO 
export interface TopUsagePlayerDto {
  teamId: number
  teamAbbr: string

  playerId: number
  playerName: string

  usagePct: number
  rank?: number
}
