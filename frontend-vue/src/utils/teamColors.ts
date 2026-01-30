//These are not the offical colors but they were chosen to look good on the dark background
export const TEAM_COLORS: Record<string, string> = {
  ATL: '#FF5A5F',
  BOS: '#22C55E',
  BKN: '#E5E7EB',
  CHA: '#7C7EFF',
  CHI: '#FF4D4F',
  CLE: '#C084FC',
  DAL: '#38BDF8',
  DEN: '#60A5FA',
  DET: '#F87171',
  GSW: '#60A5FA',
  HOU: '#FB7185',
  IND: '#38BDF8',
  LAC: '#F87171',
  LAL: '#A78BFA',
  MEM: '#7DD3FC',
  MIA: '#FB7185',
  MIL: '#34D399',
  MIN: '#60A5FA',
  NOP: '#93C5FD',
  NYK: '#60A5FA',
  OKC: '#38BDF8',
  ORL: '#38BDF8',
  PHI: '#60A5FA',
  PHX: '#C084FC',
  POR: '#FB7185',
  SAC: '#A78BFA',
  SAS: '#CBD5E1',
  TOR: '#FB7185',
  UTA: '#38BDF8',
  WAS: '#60A5FA',
}


export function teamColor(abbr?: string) {
  const key = (abbr ?? '').trim().toUpperCase()
  return TEAM_COLORS[key] ?? '#94A3B8'
}
