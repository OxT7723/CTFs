import os
import sqlite3
import secrets
import datetime
from typing import Optional, Dict, Any, List
from werkzeug.security import generate_password_hash, check_password_hash

DATABASE_PATH = "/data/forum.db"

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS direct_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    is_fake INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id)
);

CREATE TABLE IF NOT EXISTS admin_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL
);
"""

def get_db_connection(db_path: str = DATABASE_PATH) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    conn = get_db_connection()
    try:
        conn.executescript(SCHEMA_SQL)
        conn.commit()
    finally:
        conn.close()

def ensure_admin():
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_password = os.getenv("ADMIN_PASSWORD", "default_admin_pass")
    
    conn = get_db_connection()
    try:
        cur = conn.execute("SELECT id, is_admin FROM users WHERE username = ?", (admin_username,))
        row = cur.fetchone()
        if row is None:
            password_hash = generate_password_hash(admin_password)
            conn.execute(
                "INSERT INTO users (username, password_hash, is_admin, created_at) VALUES (?, ?, 1, ?)",
                (admin_username, password_hash, datetime.datetime.utcnow().isoformat()),
            )
            conn.commit()
        else:
            if row["is_admin"] != 1:
                conn.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (row["id"],))
            password_hash = generate_password_hash(admin_password)
            conn.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, row["id"]))
            conn.commit()
    finally:
        conn.close()

def ensure_fake_users():
    fake_users = [
        ("PixelCrusher89", 
         "Hey! I've been trying to get admin access for weeks. I've been moderating several communities for years and really want to learn from experienced admins here. I promise I'll be active and contribute to discussions. Please consider granting me admin privileges!",
         secrets.token_urlsafe(32)),
        ("backend_wizard", 
         "Hi Admin, I run a small Discord server with 500+ members and would love to join this forum to learn best practices from other admins. I've heard great things about the discussions here. Could you please grant me admin access? I'd really appreciate it!",
         secrets.token_urlsafe(32)),
        ("IndieDev_Kyle", 
         "Hello! A friend told me about this exclusive admin forum and I'm very interested in joining. I help moderate a subreddit and would love to connect with other community leaders. Is there any chance you could grant me admin status? Thanks for considering!",
         secrets.token_urlsafe(32)),
    ]
    
    conn = get_db_connection()
    try:
        for username, message, password in fake_users:
            cur = conn.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cur.fetchone() is None:
                password_hash = generate_password_hash(password)
                conn.execute(
                    "INSERT INTO users (username, password_hash, is_admin, created_at) VALUES (?, ?, 0, ?)",
                    (username, password_hash, datetime.datetime.utcnow().isoformat()),
                )
                conn.commit()
                
                cur = conn.execute("SELECT id FROM users WHERE username = ?", (username,))
                user_id = cur.fetchone()["id"]
                
                conn.execute(
                    "INSERT INTO direct_messages (user_id, message, is_fake, created_at) VALUES (?, ?, 1, ?)",
                    (user_id, message, datetime.datetime.utcnow().isoformat()),
                )
                conn.commit()
    finally:
        conn.close()

def create_user(username: str, password: str) -> bool:
    conn = get_db_connection()
    try:
        password_hash = generate_password_hash(password)
        conn.execute(
            "INSERT INTO users (username, password_hash, is_admin, created_at) VALUES (?, ?, 0, ?)",
            (username, password_hash, datetime.datetime.utcnow().isoformat()),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username: str, password: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    try:
        cur = conn.execute("SELECT id, username, password_hash, is_admin FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row and check_password_hash(row["password_hash"], password):
            return {"id": row["id"], "username": row["username"], "is_admin": bool(row["is_admin"])}
        return None
    finally:
        conn.close()

def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    try:
        cur = conn.execute("SELECT id, username, is_admin FROM users WHERE id = ?", (user_id,))
        row = cur.fetchone()
        if row:
            return {"id": row["id"], "username": row["username"], "is_admin": bool(row["is_admin"])}
        return None
    finally:
        conn.close()

def upsert_dm(user_id: int, message: str):
    conn = get_db_connection()
    try:
        cur = conn.execute("SELECT id FROM direct_messages WHERE user_id = ? AND is_fake = 0", (user_id,))
        if cur.fetchone():
            conn.execute(
                "UPDATE direct_messages SET message = ?, created_at = ? WHERE user_id = ? AND is_fake = 0",
                (message, datetime.datetime.utcnow().isoformat(), user_id),
            )
        else:
            conn.execute(
                "INSERT INTO direct_messages (user_id, message, is_fake, created_at) VALUES (?, ?, 0, ?)",
                (user_id, message, datetime.datetime.utcnow().isoformat()),
            )
        conn.commit()
    finally:
        conn.close()

def get_all_dms() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    try:
        cur = conn.execute("""
            SELECT u.username, u.is_admin, dm.message, dm.created_at
            FROM direct_messages dm 
            JOIN users u ON dm.user_id = u.id 
            ORDER BY dm.id
        """)
        results = []
        for row in cur.fetchall():
            created_at = row["created_at"]
            date_only = created_at.split('T')[0] if 'T' in created_at else created_at.split()[0]
            
            results.append({
                "username": row["username"],
                "message": row["message"],
                "date": date_only,
                "is_admin": bool(row["is_admin"])
            })
        return results
    finally:
        conn.close()

def delete_non_fake_dms():
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM direct_messages WHERE is_fake = 0")
        conn.commit()
    finally:
        conn.close()

def append_admin_message(role: str, content: str):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO admin_messages (role, content, created_at) VALUES (?, ?, ?)",
            (role, content, datetime.datetime.utcnow().isoformat()),
        )
        conn.commit()
    finally:
        conn.close()

def get_admin_messages(limit: int = 50) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    try:
        cur = conn.execute(
            "SELECT id, role, content, created_at FROM admin_messages ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        rows = [dict(row) for row in cur.fetchall()]
        rows.reverse()
        return rows
    finally:
        conn.close()

def clear_admin_messages():
    conn = get_db_connection()
    try:
        conn.execute("DELETE FROM admin_messages")
        conn.commit()
    finally:
        conn.close()

def make_user_admin(username: str) -> bool:
    conn = get_db_connection()
    try:
        cur = conn.execute("SELECT id FROM users WHERE username = ?", (username,))
        row = cur.fetchone()
        if row is None:
            return False
        conn.execute("UPDATE users SET is_admin = 1 WHERE id = ?", (row["id"],))
        conn.commit()
        return True
    finally:
        conn.close()
