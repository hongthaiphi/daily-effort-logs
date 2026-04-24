"""Database module - SQLite operations"""
import sqlite3
import os
from datetime import datetime
from typing import List, Optional, Tuple

DB_PATH = "effort_tracker.db"

def init_db():
    """Initialize database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            chat_id INTEGER UNIQUE,
            username TEXT,
            first_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Daily scores table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date DATE NOT NULL,
            score INTEGER NOT NULL CHECK(score >= 1 AND score <= 10),
            diary TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            UNIQUE(user_id, date)
        )
    ''')

    conn.commit()
    conn.close()

def add_user(chat_id: int, username: str = None, first_name: str = None):
    """Add or update user"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        cursor.execute('''
            INSERT INTO users (chat_id, username, first_name)
            VALUES (?, ?, ?)
        ''', (chat_id, username, first_name))
        conn.commit()
    except sqlite3.IntegrityError:
        # User already exists, update
        cursor.execute('''
            UPDATE users SET username = ?, first_name = ?
            WHERE chat_id = ?
        ''', (username, first_name, chat_id))
        conn.commit()

    conn.close()

def get_user_id(chat_id: int) -> Optional[int]:
    """Get user_id from chat_id"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE chat_id = ?', (chat_id,))
    result = cursor.fetchone()
    conn.close()

    return result[0] if result else None

def save_score(chat_id: int, score: int, diary: str = ""):
    """Save daily score and diary"""
    user_id = get_user_id(chat_id)
    if not user_id:
        return False

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    today = datetime.now().date()

    try:
        cursor.execute('''
            INSERT INTO daily_scores (user_id, date, score, diary)
            VALUES (?, ?, ?, ?)
        ''', (user_id, today, score, diary))
        conn.commit()
    except sqlite3.IntegrityError:
        # Update existing score for today
        cursor.execute('''
            UPDATE daily_scores
            SET score = ?, diary = ?, created_at = CURRENT_TIMESTAMP
            WHERE user_id = ? AND date = ?
        ''', (score, diary, user_id, today))
        conn.commit()

    conn.close()
    return True

def get_today_score(chat_id: int) -> Optional[Tuple[int, str]]:
    """Get today's score and diary"""
    user_id = get_user_id(chat_id)
    if not user_id:
        return None

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    today = datetime.now().date()

    cursor.execute('''
        SELECT score, diary FROM daily_scores
        WHERE user_id = ? AND date = ?
    ''', (user_id, today))

    result = cursor.fetchone()
    conn.close()

    return result

def get_scores_range(chat_id: int, days: int = 30) -> List[Tuple[str, int, str]]:
    """Get scores for last N days (date, score, diary)"""
    user_id = get_user_id(chat_id)
    if not user_id:
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT date, score, diary FROM daily_scores
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT ?
    ''', (user_id, days))

    results = cursor.fetchall()
    conn.close()

    return results

def get_stats(chat_id: int, days: int = 30) -> dict:
    """Get statistics for last N days"""
    user_id = get_user_id(chat_id)
    if not user_id:
        return {}

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            AVG(score) as avg_score,
            MAX(score) as max_score,
            MIN(score) as min_score,
            COUNT(*) as total_days
        FROM daily_scores
        WHERE user_id = ? AND date >= date('now', '-' || ? || ' days')
    ''', (user_id, days))

    result = cursor.fetchone()
    conn.close()

    if result and result[3]:  # Has data
        return {
            'avg_score': round(result[0], 2),
            'max_score': result[1],
            'min_score': result[2],
            'total_days': result[3]
        }

    return {'avg_score': 0, 'max_score': 0, 'min_score': 0, 'total_days': 0}

def get_all_users() -> List[int]:
    """Get all active chat_ids"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT chat_id FROM users')
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results
