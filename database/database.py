import sqlite3
from pathlib import Path
import requests

BASE_DIR = Path(__name__).resolve().parent

class DatabaseConnection:
    def __init__(self, database_path: str) -> None:
        self.database_path = database_path
        self.cursor, self.connection = self.connect()


    def connect(self) -> tuple[sqlite3.Cursor, sqlite3.Connection]:
        connection = sqlite3.connect(BASE_DIR / self.database_path)
        cursor = connection.cursor()
        return cursor, connection

class DatabaseTables(DatabaseConnection):
    def __init__(self, database_path: str) -> None:
        super().__init__(database_path)

    def create(self, query:str) -> None:
        self.cursor.executescript(query)

db_table = DatabaseTables('database.db')
db_table.create('''
CREATE TABLE IF NOT EXISTS admins(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    chat_id BIGINT UNIQUE,
    username TEXT UNIQUE,
    role TEXT
);
CREATE TABLE IF NOT EXISTS media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    file_id TEXT UNIQUE, 
    title TEXT,
    category TEXT CHECK(category IN ('movies','cartoons','dramas','anime')),
    genre TEXT
);
''')

class AdminsRepo(DatabaseConnection):
    def get_admin(self, chat_id):
        self.cursor.execute("SELECT id FROM admins WHERE chat_id = ?;", (chat_id,))
        result = self.cursor.fetchone()
        return result

    def add_main_admin(self, chat_id,username):
        query = 'INSERT INTO admins(chat_id,username,role) VALUES(?,?,?);'

        if self.get_admin(chat_id) is None:
            self.cursor.execute(query, (chat_id,username,'main',))
            self.connection.commit()

    def add_admins(self,chat_id,username,role):
        query = 'INSERT INTO admins(chat_id,username,role) VALUES(?,?,?);'
        if self.get_admin(chat_id) is None:
            self.cursor.execute(query, (chat_id, username,role,))
            self.connection.commit()
            return True
        else:
            return False

    def get_admin_list(self):
        self.cursor.execute("SELECT * FROM admins;",)
        result = self.cursor.fetchall()
        return result

    def delete_admin(self,admin_id):
        query = "DELETE FROM admins WHERE id = ?;"
        self.cursor.execute(query, (admin_id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def check_admin_role(self,chat_id):
        self.cursor.execute("SELECT role FROM admins WHERE chat_id = ?;",(chat_id,) )
        result = self.cursor.fetchone()
        return result[0]


class MediaRepo(DatabaseConnection):
    def media_exists(self, title, file_id):
        self.cursor.execute("SELECT * FROM media WHERE title = ? OR file_id = ?", (title, file_id))
        return self.cursor.fetchone() is not None

    def add_media(self, title, file_id, category, genre):
        if self.media_exists(title, file_id):
            return False

        self.cursor.execute("INSERT INTO media (file_id,title, category, genre) VALUES (?, ?, ?, ?)", (file_id, title, category, genre))
        self.connection.commit()
        return True

    def get_files_by_category(self,category):
        self.cursor.execute("SELECT id, file_id, title, genre FROM media WHERE category = ?", (category,))
        result = self.cursor.fetchall()
        return result

    def delete_file(self, id):
        self.cursor.execute("DELETE FROM media WHERE id = ?", (id,))
        self.connection.commit()
        return self.cursor.rowcount > 0

    def search_media_id(self, id, category):
        self.cursor.execute('SELECT file_id, title, genre FROM media WHERE id = ? AND category = ?',(id,category,))
        result = self.cursor.fetchone()
        return result

    def search_media_title(self, title, category):
        self.cursor.execute('SELECT file_id, title, genre FROM media WHERE title LIKE ? AND category = ?',(f"%{title}%",category,))
        result = self.cursor.fetchall()
        return result

    def search_media_genre(self, genre, category):
        self.cursor.execute('SELECT file_id, title, genre FROM media WHERE genre LIKE ? AND category = ?',
                            (f"%{genre}%", category,))
        result = self.cursor.fetchall()
        return result


admin_repo = AdminsRepo(BASE_DIR/'database.db')
media_repo = MediaRepo(BASE_DIR/'database.db')