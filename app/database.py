
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "smartops.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            method TEXT,
            endpoint TEXT,
            status_code INTEGER,
            response_time REAL
        )
    """)

    conn.commit()
    conn.close()


def save_monitoring_log(timestamp, method, endpoint,
                        status_code, response_time):

    conn = get_connection()

    conn.execute("""
        INSERT INTO monitoring_logs
        (timestamp, method, endpoint, status_code, response_time)
        VALUES (?, ?, ?, ?, ?)
    """, (timestamp, method, endpoint, status_code, response_time))

    conn.commit()
    conn.close()


def get_monitoring_logs():
    conn = get_connection()

    rows = conn.execute("""
        SELECT * FROM monitoring_logs
        ORDER BY id DESC
    """).fetchall()

    conn.close()

    return [dict(row) for row in rows]


def get_monitoring_stats():
    conn = get_connection()

    result = conn.execute("""
        SELECT
            COUNT(*) AS total_requests,

            SUM(CASE
                WHEN status_code >= 200 AND status_code < 400
                THEN 1 ELSE 0
            END) AS successful_requests,

            SUM(CASE
                WHEN status_code >= 400
                THEN 1 ELSE 0
            END) AS failed_requests,

            ROUND(AVG(response_time), 2) AS avg_response_time,

            ROUND(MAX(response_time), 2) AS max_response_time,

            SUM(CASE
                WHEN response_time > 500
                THEN 1 ELSE 0
            END) AS slow_requests

        FROM monitoring_logs
    """).fetchone()

    conn.close()

    return {
        "total_requests": result["total_requests"] or 0,
        "successful_requests": result["successful_requests"] or 0,
        "failed_requests": result["failed_requests"] or 0,
        "avg_response_time": result["avg_response_time"] or 0,
        "max_response_time": result["max_response_time"] or 0,
        "slow_requests": result["slow_requests"] or 0
    }

