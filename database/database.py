import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os

BASE_DIR = Path(__file__).resolve().parent
load_dotenv()


class DatabaseConnection:
    def __init__(self):
        self._connect()

    def _connect(self):
        """Establish a new database connection."""
        self.connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5
        )
        self.cursor = self.connection.cursor()

    def ensure_connection(self):
        """Reconnect if connection is closed."""
        if self.connection is None or self.connection.closed != 0:
            print("[DB] Reconnecting to database...")
            self._connect()


class DatabaseTables(DatabaseConnection):
    def create(self, query: str) -> None:
        self.ensure_connection()
        try:
            self.cursor.execute(query)
            self.connection.commit()
        except Exception as e:
            print(f"[DB ERROR] create(): {e}")
            self.connection.rollback()


db_table = DatabaseTables()
db_table.create("""
CREATE TABLE IF NOT EXISTS admins(
    id SERIAL PRIMARY KEY,
    chat_id BIGINT UNIQUE,
    username TEXT UNIQUE,
    role TEXT
);
CREATE TABLE IF NOT EXISTS media (
    id SERIAL PRIMARY KEY,
    file_id TEXT UNIQUE,
    title TEXT,
    category TEXT CHECK(category IN ('movies','cartoons','dramas','anime')),
    genre TEXT
);
""")


class AdminsRepo(DatabaseConnection):
    def get_admin(self, chat_id):
        self.ensure_connection()
        try:
            self.cursor.execute("SELECT id FROM admins WHERE chat_id = %s;", (chat_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"[DB ERROR] get_admin(): {e}")
            self.connection.rollback()
            return None

    def add_main_admin(self, chat_id, username):
        self.ensure_connection()
        try:
            if self.get_admin(chat_id) is None:
                self.cursor.execute(
                    "INSERT INTO admins(chat_id, username, role) VALUES(%s, %s, %s);",
                    (chat_id, username, 'main')
                )
                self.connection.commit()
        except Exception as e:
            print(f"[DB ERROR] add_main_admin(): {e}")
            self.connection.rollback()

    def add_admins(self, chat_id, username, role):
        self.ensure_connection()
        try:
            if self.get_admin(chat_id) is None:
                self.cursor.execute(
                    "INSERT INTO admins(chat_id, username, role) VALUES(%s, %s, %s);",
                    (chat_id, username, role)
                )
                self.connection.commit()
                return True
        except Exception as e:
            print(f"[DB ERROR] add_admins(): {e}")
            self.connection.rollback()
        return False

    def get_admin_list(self):
        self.ensure_connection()
        try:
            self.cursor.execute("SELECT * FROM admins;")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[DB ERROR] get_admin_list(): {e}")
            self.connection.rollback()
            return []

    def delete_admin(self, admin_id):
        self.ensure_connection()
        try:
            self.cursor.execute("DELETE FROM admins WHERE id = %s;", (admin_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"[DB ERROR] delete_admin(): {e}")
            self.connection.rollback()
            return False

    def check_admin_role(self, chat_id):
        self.ensure_connection()
        try:
            self.cursor.execute("SELECT role FROM admins WHERE chat_id = %s;", (chat_id,))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"[DB ERROR] check_admin_role(): {e}")
            self.connection.rollback()
            return None


class MediaRepo(DatabaseConnection):
    def media_exists(self, title, file_id):
        self.ensure_connection()
        try:
            self.cursor.execute(
                "SELECT 1 FROM media WHERE title = %s OR file_id = %s;", (title, file_id)
            )
            return self.cursor.fetchone() is not None
        except Exception as e:
            print(f"[DB ERROR] media_exists(): {e}")
            self.connection.rollback()
            return False

    def add_media(self, title, file_id, category, genre):
        self.ensure_connection()
        try:
            if self.media_exists(title, file_id):
                return False
            self.cursor.execute(
                "INSERT INTO media (file_id, title, category, genre) VALUES (%s, %s, %s, %s);",
                (file_id, title, category, genre)
            )
            self.connection.commit()
            return True
        except Exception as e:
            print(f"[DB ERROR] add_media(): {e}")
            self.connection.rollback()
            return False

    def get_files_by_category(self, category):
        self.ensure_connection()
        try:
            self.cursor.execute(
                "SELECT id, file_id, title, genre FROM media WHERE category = %s;", (category,)
            )
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[DB ERROR] get_files_by_category(): {e}")
            self.connection.rollback()
            return []

    def delete_file(self, file_id):
        self.ensure_connection()
        try:
            self.cursor.execute("DELETE FROM media WHERE id = %s;", (file_id,))
            self.connection.commit()
            return self.cursor.rowcount > 0
        except Exception as e:
            print(f"[DB ERROR] delete_file(): {e}")
            self.connection.rollback()
            return False

    def search_media_id(self, id, category):
        self.ensure_connection()
        try:
            self.cursor.execute(
                "SELECT file_id, title, genre FROM media WHERE id = %s AND category = %s;",
                (id, category)
            )
            return self.cursor.fetchone()
        except Exception as e:
            print(f"[DB ERROR] search_media_id(): {e}")
            self.connection.rollback()
            return None

    def search_media_title(self, title, category):
        self.ensure_connection()
        try:
            self.cursor.execute(
                "SELECT file_id, title, genre FROM media WHERE title ILIKE %s AND category = %s;",
                (f"%{title}%", category)
            )
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[DB ERROR] search_media_title(): {e}")
            self.connection.rollback()
            return []

    def search_media_genre(self, genre, category):
        self.ensure_connection()
        try:
            self.cursor.execute(
                "SELECT file_id, title, genre FROM media WHERE genre ILIKE %s AND category = %s;",
                (f"%{genre}%", category)
            )
            return self.cursor.fetchall()
        except Exception as e:
            print(f"[DB ERROR] search_media_genre(): {e}")
            self.connection.rollback()
            return []


# ✅ Instantiate Repos
admin_repo = AdminsRepo()
media_repo = MediaRepo()
