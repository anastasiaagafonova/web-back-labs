import sqlite3
import json
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

class UserModel:
    def __init__(self, db):
        self.db = db
    
    def create_user(self, username, password):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO snow_users (username, password_hash) VALUES (?, ?)",
                (username, generate_password_hash(password))
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()
    
    def get_user_by_username(self, username):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM snow_users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        return dict(user) if user else None
    
    def check_password(self, user, password):
        return check_password_hash(user['password_hash'], password)

class GiftModel:
    def __init__(self, db):
        self.db = db
    
    def init_gifts(self):
        """Инициализация 10 подарков с поздравлениями и картинками"""
        gifts = [
            (1, "С Новым годом! Пусть сбудутся все мечты!", "gift1.jpg", "box1.jpg", 0),
            (2, "Желаю здоровья, счастья и удачи в новом году!", "gift2.jpg", "box2.jpg", 0),
            (3, "Пусть новый год принесет много радостных моментов!", "gift3.jpg", "box3.jpg", 1),
            (4, "Счастья, любви и процветания в новом году!", "gift4.jpg", "box4.jpg", 0),
            (5, "Мечтай, дерзай, достигай! С Новым годом!", "gift5.jpg", "box5.jpg", 0),
            (6, "Пусть ангел-хранитель оберегает тебя весь год!", "gift6.jpg", "box6.jpg", 1),
            (7, "Новых достижений и ярких впечатлений!", "gift7.jpg", "box7.jpg", 0),
            (8, "Пусть каждый день будет наполнен счастьем!", "gift8.jpg", "box8.jpg", 0),
            (9, "Успехов во всех начинаниях! С Новым годом!", "gift9.jpg", "box9.jpg", 1),
            (10, "Гармонии, уюта и семейного тепла!", "gift10.jpg", "box10.jpg", 0)
        ]
        
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        # Проверяем, есть ли уже подарки
        cursor.execute("SELECT COUNT(*) FROM snow_gifts")
        count = cursor.fetchone()[0]
        
        if count == 0:
            for gift_number, message, gift_image, box_image, requires_auth in gifts:
                cursor.execute(
                    """INSERT INTO snow_gifts 
                       (gift_number, message, gift_image, box_image, requires_auth) 
                       VALUES (?, ?, ?, ?, ?)""",
                    (gift_number, message, gift_image, box_image, requires_auth)
                )
        
        conn.commit()
        conn.close()
    
    def get_all_gifts(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM snow_gifts ORDER BY gift_number")
        gifts = cursor.fetchall()
        conn.close()
        # Преобразуем Row в словари
        return [dict(gift) for gift in gifts]
    
    def get_gift(self, gift_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM snow_gifts WHERE id = ?", (gift_id,))
        gift = cursor.fetchone()
        conn.close()
        return dict(gift) if gift else None
    
    def mark_as_opened(self, gift_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE snow_gifts SET is_opened = 1 WHERE id = ?",
            (gift_id,)
        )
        conn.commit()
        conn.close()
    
    def reset_all_gifts(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE snow_gifts SET is_opened = 0")
        cursor.execute("DELETE FROM snow_user_gifts")
        conn.commit()
        conn.close()

class UserGiftModel:
    def __init__(self, db):
        self.db = db
    
    def add_opened_gift(self, user_id, session_id, gift_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO snow_user_gifts (user_id, session_id, gift_id) 
               VALUES (?, ?, ?)""",
            (user_id, session_id, gift_id)
        )
        conn.commit()
        conn.close()
    
    def get_opened_gifts_count(self, user_id=None, session_id=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute(
                "SELECT COUNT(*) FROM snow_user_gifts WHERE user_id = ?",
                (user_id,)
            )
        else:
            cursor.execute(
                "SELECT COUNT(*) FROM snow_user_gifts WHERE session_id = ?",
                (session_id,)
            )
        
        count = cursor.fetchone()[0]
        conn.close()
        return count
    
    def get_opened_gifts(self, user_id=None, session_id=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute(
                """SELECT gift_id FROM snow_user_gifts 
                   WHERE user_id = ?""",
                (user_id,)
            )
        else:
            cursor.execute(
                """SELECT gift_id FROM snow_user_gifts 
                   WHERE session_id = ?""",
                (session_id,)
            )
        
        gifts = cursor.fetchall()
        conn.close()
        return [gift[0] for gift in gifts]
    
    def clear_user_gifts(self, user_id=None, session_id=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        if user_id:
            cursor.execute(
                "DELETE FROM snow_user_gifts WHERE user_id = ?",
                (user_id,)
            )
        else:
            cursor.execute(
                "DELETE FROM snow_user_gifts WHERE session_id = ?",
                (session_id,)
            )
        
        conn.commit()
        conn.close()