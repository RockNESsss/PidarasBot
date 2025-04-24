import sqlite3
from datetime import datetime

DB_PATH = "db/pidarometer.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, telegram_id INTEGER UNIQUE, username TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS circles (id INTEGER PRIMARY KEY, name TEXT, creator_id INTEGER)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS circle_members (id INTEGER PRIMARY KEY, circle_id INTEGER, user_id INTEGER, role TEXT)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS people (id INTEGER PRIMARY KEY, circle_id INTEGER, name TEXT,
                    komandnist INTEGER DEFAULT 0, kritichnist INTEGER DEFAULT 0, vidpovidalnist INTEGER DEFAULT 0,
                    korisnist INTEGER DEFAULT 0, samoocinka INTEGER DEFAULT 0)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS proposals (id INTEGER PRIMARY KEY, circle_id INTEGER, person_name TEXT,
                    category TEXT, delta INTEGER, comment TEXT, proposer_id INTEGER, timestamp TEXT, voted INTEGER DEFAULT 0)""")
    cur.execute("""CREATE TABLE IF NOT EXISTS votes (id INTEGER PRIMARY KEY, proposal_id INTEGER, voter_id INTEGER, vote_type TEXT)""")
    conn.commit()
    conn.close()

def add_user(telegram_id, username):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?)", (telegram_id, username))
    conn.commit()
    conn.close()

def get_user_id(telegram_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE telegram_id=?", (telegram_id,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def get_user_circle(user_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT circle_id FROM circle_members WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else None

def get_user_role(user_id, circle_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT role FROM circle_members WHERE user_id=? AND circle_id=?", (user_id, circle_id))
    result = cur.fetchone()
    conn.close()
    return result[0] if result else "member"

def create_circle(name, creator_id):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("INSERT INTO circles (name, creator_id) VALUES (?, ?)", (name, creator_id))
    conn.commit()
    circle_id = cur.lastrowid
    cur.execute("INSERT INTO circle_members (circle_id, user_id, role) VALUES (?, ?, 'admin')", (circle_id, creator_id))
    conn.commit()
    conn.close()
    return circle_id
