import pytest

pytestmark = pytest.mark.db

def test_nba_teams_team_id_unique(db_cursor):
    db_cursor.execute("SELECT COUNT(*) FROM nba_teams")
    (total,) = db_cursor.fetchone()
    db_cursor.execute("SELECT COUNT(DISTINCT team_id) FROM nba_teams")
    (distinct_total,) = db_cursor.fetchone()
    assert total == distinct_total

def test_top_usage_players_team_id_fk(db_cursor):
    db_cursor.execute("""
        SELECT COUNT(*)
        FROM top_usage_players t
        LEFT JOIN nba_teams n ON n.team_id = t.team_id
        WHERE n.team_id IS NULL
    """)
    (orphans,) = db_cursor.fetchone()
    assert orphans == 0

def test_defensive_efficiency_team_id_fk(db_cursor):
    db_cursor.execute("""
        SELECT COUNT(*)
        FROM defensive_efficiency d
        LEFT JOIN nba_teams n ON n.team_id = d.team_id
        WHERE n.team_id IS NULL
    """)
    (orphans,) = db_cursor.fetchone()
    assert orphans == 0

def test_top_usage_players_usage_ranges(db_cursor): # Usage % between 0 and 100
    db_cursor.execute("""
        SELECT COUNT(*)
        FROM top_usage_players
        WHERE (player1_usage IS NOT NULL AND (player1_usage < 0 OR player1_usage > 100))
           OR (player2_usage IS NOT NULL AND (player2_usage < 0 OR player2_usage > 100))
           OR (player3_usage IS NOT NULL AND (player3_usage < 0 OR player3_usage > 100))
           OR (player4_usage IS NOT NULL AND (player4_usage < 0 OR player4_usage > 100))
           OR (player5_usage IS NOT NULL AND (player5_usage < 0 OR player5_usage > 100))
    """)
    (bad,) = db_cursor.fetchone()
    assert bad == 0

def test_top_usage_players_name_usage_pairing(db_cursor): #If usage exists, the corresponding name must exist
    db_cursor.execute("""
        SELECT COUNT(*)
        FROM top_usage_players
        WHERE (player1_name IS NULL AND player1_usage IS NOT NULL)
           OR (player2_name IS NULL AND player2_usage IS NOT NULL)
           OR (player3_name IS NULL AND player3_usage IS NOT NULL)
           OR (player4_name IS NULL AND player4_usage IS NOT NULL)
           OR (player5_name IS NULL AND player5_usage IS NOT NULL)
    """)
    (bad,) = db_cursor.fetchone()
    assert bad == 0

def test_positions_required_fields(db_cursor):
    db_cursor.execute("""
        SELECT COUNT(*)
        FROM positions
        WHERE player_name IS NULL OR player_position IS NULL
    """)
    (nulls,) = db_cursor.fetchone()
    assert nulls == 0

def test_positions_allowed_values(db_cursor):
    db_cursor.execute("""
        SELECT COUNT(*)
        FROM positions
        WHERE player_position NOT IN ('G','G-F', 'F-G','F','F-C', 'C-F','C')
    """)
    (bad,) = db_cursor.fetchone()
    assert bad == 0

def test_defensive_efficiency_ranges(db_cursor): # Defensive efficiency must be non-negative and reasonable (0-200)
    db_cursor.execute("""
        SELECT COUNT(*)
        FROM defensive_efficiency
        WHERE (pg_efficiency IS NOT NULL AND (pg_efficiency < 0 OR pg_efficiency > 200))
           OR (sg_efficiency IS NOT NULL AND (sg_efficiency < 0 OR sg_efficiency > 200))
           OR (sf_efficiency IS NOT NULL AND (sf_efficiency < 0 OR sf_efficiency > 200))
           OR (pf_efficiency IS NOT NULL AND (pf_efficiency < 0 OR pf_efficiency > 200))
           OR (c_efficiency IS NOT NULL AND (c_efficiency < 0 OR c_efficiency > 200))
    """)
    (bad,) = db_cursor.fetchone()
    assert bad == 0

def test_averages_required_fields(db_cursor):
    db_cursor.execute("""
        SELECT COUNT(*)
        FROM averages
        WHERE player_name IS NULL
           OR player_pts IS NULL
           OR player_reb IS NULL
           OR player_ast IS NULL
           OR player_pra IS NULL
    """)
    (nulls,) = db_cursor.fetchone()
    assert nulls == 0

def test_averages_non_negative(db_cursor):
    db_cursor.execute("""
        SELECT COUNT(*)
        FROM averages
        WHERE player_pts < 0 OR player_reb < 0 OR player_ast < 0 OR player_pra < 0
    """)
    (bad,) = db_cursor.fetchone()
    assert bad == 0

def test_games_required_fields_and_scores(db_cursor):
    db_cursor.execute("""
        SELECT COUNT(*)
        FROM games
        WHERE game_date IS NULL
    """)
    (nulls,) = db_cursor.fetchone()
    assert nulls == 0

    db_cursor.execute("""
        SELECT COUNT(*)
        FROM games
        WHERE (home_team_score IS NOT NULL AND home_team_score < 0)
           OR (away_team_score IS NOT NULL AND away_team_score < 0)
    """)
    (bad,) = db_cursor.fetchone()
    assert bad == 0
