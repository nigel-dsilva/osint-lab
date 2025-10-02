import sqlite3
from pathlib import Path
from typing import List, Tuple, Any
from src.utils.env import load

def get_db_path() -> Path:
    cfg = load()
    db_path = Path(cfg['project']['storage_dir']) / "osint.db"
    db_path.parent.mkdir(parents=True, exist_ok=True)
    return db_path

def init_db():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS indicators (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        indicator TEXT,
        type TEXT,
        first_seen TEXT,
        last_seen TEXT,
        source TEXT,
        confidence TEXT,
        score INTEGER,
        country TEXT,
        asn TEXT
    )
    """)
    conn.commit()
    conn.close()

def insert_many(records: List[Tuple[Any]]):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executemany("""
    INSERT INTO indicators
    (indicator, type, first_seen, last_seen, source, confidence, score, country, asn)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, records)
    conn.commit()
    conn.close()

def query(sql: str, params: Tuple = ()):
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()
    return rows
