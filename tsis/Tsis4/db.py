import psycopg2


DB_PARAMS = {
    "dbname": "snake_db",
    "user": "postgres",
    "password": 12345678,
    "host": "localhost"
}

def get_connection():
    return psycopg2.connect(**DB_PARAMS)

def save_game_result(username, score, level):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    player_id = cur.fetchone()[0]
    
    cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", 
                (player_id, score, level))
    conn.commit()
    cur.close()
    conn.close()

def get_top_scores():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT p.username, s.score, s.level_reached 
        FROM game_sessions s JOIN players p ON s.player_id = p.id 
        ORDER BY s.score DESC LIMIT 10
    """)
    rows = cur.fetchall()
    conn.close()
    return rows

def get_personal_best(username):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT MAX(score) FROM game_sessions s 
        JOIN players p ON s.player_id = p.id WHERE p.username = %s
    """, (username,))
    res = cur.fetchone()[0]
    conn.close()
    return res if res else 0