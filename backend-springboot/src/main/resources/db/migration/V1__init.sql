CREATE TABLE IF NOT EXISTS top_usage_players (
  team_id INTEGER PRIMARY KEY,
  player1_name TEXT,
  player1_usage DOUBLE PRECISION,
  player2_name TEXT,
  player2_usage DOUBLE PRECISION,
  player3_name TEXT,
  player3_usage DOUBLE PRECISION,
  player4_name TEXT,
  player4_usage DOUBLE PRECISION,
  player5_name TEXT,
  player5_usage DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS positions (
  id SERIAL PRIMARY KEY,
  player_name TEXT,
  player_position TEXT
);

CREATE TABLE IF NOT EXISTS defensive_efficiency (
  team_id INTEGER PRIMARY KEY,
  pg_efficiency DOUBLE PRECISION,
  sg_efficiency DOUBLE PRECISION,
  sf_efficiency DOUBLE PRECISION,
  pf_efficiency DOUBLE PRECISION,
  c_efficiency DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS averages (
  id SERIAL PRIMARY KEY,
  player_name TEXT,
  player_pts DOUBLE PRECISION,
  player_reb DOUBLE PRECISION,
  player_ast DOUBLE PRECISION,
  player_pra DOUBLE PRECISION
);