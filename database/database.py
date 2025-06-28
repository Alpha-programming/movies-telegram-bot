import psycopg2
from pathlib import Path
from dotenv import load_dotenv
import os
BASE_DIR = Path(__file__).resolve().parent
load_dotenv()


class DatabaseConnection:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT")
        )
        self.cursor = self.connection.cursor()


class DatabaseTables(DatabaseConnection):
    def create(self, query: str) -> None:
        self.cursor.execute(query)
        self.connection.commit()


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
        self.cursor.execute("SELECT id FROM admins WHERE chat_id = %s;", (chat_id,))
        return self.cursor.fetchone()

    def add_main_admin(self, chat_id, username):
        if self.get_admin(chat_id) is None:
            self.cursor.execute(
                "INSERT INTO admins(chat_id, username, role) VALUES(%s, %s, %s);",
                (chat_id, username, 'main')
            )
            self.connection.commit()

    def add_admins(self, chat_id, username, role):
        if self.get_admin(chat_id) is None:
            self.cursor.execute(
                "INSERT INTO admins(chat_id, username, role) VALUES(%s, %s, %s);",
                (chat_id, username, role)
            )
            self.connection.commit()
            return True
        return False

    def get_admin_list(self):
        self.cursor.execute("SELECT * FROM admins;")
        return self.cursor.fetchall()

    def delete_admin(self, admin_id):
        self.cursor.execute("DELETE FROM admins WHERE id = %s;", (admin_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def check_admin_role(self, chat_id):
        self.cursor.execute("SELECT role FROM admins WHERE chat_id = %s;", (chat_id,))
        result = self.cursor.fetchone()
        return result[0] if result else None


class MediaRepo(DatabaseConnection):
    def media_exists(self, title, file_id):
        self.cursor.execute(
            "SELECT 1 FROM media WHERE title = %s OR file_id = %s;", (title, file_id)
        )
        return self.cursor.fetchone() is not None

    def add_media(self, title, file_id, category, genre):
        if self.media_exists(title, file_id):
            return False
        self.cursor.execute(
            "INSERT INTO media (file_id, title, category, genre) VALUES (%s, %s, %s, %s);",
            (file_id, title, category, genre)
        )
        self.connection.commit()
        return True

    def get_files_by_category(self, category):
        self.cursor.execute(
            "SELECT id, file_id, title, genre FROM media WHERE category = %s;", (category,)
        )
        return self.cursor.fetchall()

    def delete_file(self, file_id):
        self.cursor.execute("DELETE FROM media WHERE id = %s;", (file_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def search_media_id(self, id, category):
        self.cursor.execute(
            "SELECT file_id, title, genre FROM media WHERE id = %s AND category = %s;",
            (id, category)
        )
        return self.cursor.fetchone()

    def search_media_title(self, title, category):
        self.cursor.execute(
            "SELECT file_id, title, genre FROM media WHERE title ILIKE %s AND category = %s;",
            (f"%{title}%", category)
        )
        return self.cursor.fetchall()

    def search_media_genre(self, genre, category):
        self.cursor.execute(
            "SELECT file_id, title, genre FROM media WHERE genre ILIKE %s AND category = %s;",
            (f"%{genre}%", category)
        )
        return self.cursor.fetchall()


# ✅ Instantiate Repos
admin_repo = AdminsRepo()
media_repo = MediaRepo()
