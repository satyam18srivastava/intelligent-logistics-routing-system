
import sqlite3

DATABASE = "logistics.db"


def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                location TEXT NOT NULL,
                priority INTEGER NOT NULL,
                burst INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'Pending',
                assigned_vehicle TEXT
            )
        """)

        connection.execute("""
            CREATE TABLE IF NOT EXISTS vehicles (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL UNIQUE,
                location TEXT NOT NULL,
                status TEXT NOT NULL DEFAULT 'Available',
                current_task_id TEXT
            )
        """)


if __name__ == "__main__":
    init_db()
    print("SQLite database and tables initialized successfully.")
