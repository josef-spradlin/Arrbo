CREATE TABLE IF NOT EXISTS games (
  game_id TEXT PRIMARY KEY,
  game_date DATE NOT NULL,
  start_time_utc TIMESTAMPTZ,
  status_text TEXT,

  home_team_id INTEGER,
  home_team_abbr TEXT,
  home_team_score INTEGER,

  away_team_id INTEGER,
  away_team_abbr TEXT,
  away_team_score INTEGER
);

CREATE INDEX IF NOT EXISTS idx_games_game_date ON games (game_date);
