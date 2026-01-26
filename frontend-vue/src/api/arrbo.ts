// src/api/arrbo.ts
import http from './http'
import type { GameDto, TopUsagePlayerDto, ISODate } from '../types/dto'

export async function getGamesByDate(date: ISODate): Promise<GameDto[]> {
  const res = await http.get<GameDto[]>('/api/games', { params: { date } })
  return res.data
}

export async function getTopUsagePlayers(): Promise<TopUsagePlayerDto[]> {
  const res = await http.get<TopUsagePlayerDto[]>('/api/usage/top')
  return res.data
}
