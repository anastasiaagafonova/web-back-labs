from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import random
import os
import sqlite3
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

lab9_bp = Blueprint('lab9', __name__, template_folder='templates', static_folder='static')

DB_TYPE = os.environ.get('DB_TYPE', 'sqlite')  

if DB_TYPE == 'postgres':
    DB_CONFIG = {
        'host': os.environ.get('DB_HOST', 'localhost'),
        'port': os.environ.get('DB_PORT', '5432'),
        'database': os.environ.get('DB_NAME', 'anastasia_agafonova_knowledge_base'),
        'user': os.environ.get('DB_USER', 'postgres'),
        'password': os.environ.get('DB_PASSWORD', '')
    }
else:
    DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anastasia_agafonova_knowledge_base.db')

class Database:
    def __init__(self):
        self.db_type = DB_TYPE
        
    def get_connection(self):
        if self.db_type == 'postgres':
            conn = psycopg2.connect(**DB_CONFIG)
            conn.autocommit = False
        else:
            conn = sqlite3.connect(DB_PATH)
            conn.row_factory = sqlite3.Row
        return conn

class UserModel:
    def __init__(self, db):
        self.db = db
    
    def create_user(self, username, password):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            if self.db.db_type == 'postgres':
                cursor.execute(
                    "INSERT INTO snow_users (username, password_hash) VALUES (%s, %s)",
                    (username, generate_password_hash(password))
                )
            else:
                cursor.execute(
                    "INSERT INTO snow_users (username, password_hash) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
            conn.commit()
            return True
        except (psycopg2.IntegrityError, sqlite3.IntegrityError) as e:
            print(f"Error creating user: {e}")
            return False
        finally:
            conn.close()
    
    def get_user_by_username(self, username):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.db.db_type == 'postgres':
                cursor.execute("SELECT * FROM snow_users WHERE username = %s", (username,))
                columns = [desc[0] for desc in cursor.description]
                user = cursor.fetchone()
                if user:
                    user = dict(zip(columns, user))
            else:
                cursor.execute("SELECT * FROM snow_users WHERE username = ?", (username,))
                user = cursor.fetchone()
                if user:
                    user = dict(user)
            return user
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
        finally:
            conn.close()
    
    def check_password(self, user, password):
        if not user:
            return False
        return check_password_hash(user['password_hash'], password)

class GiftModel:
    def __init__(self, db):
        self.db = db
    
    def create_tables(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.db.db_type == 'postgres':
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS snow_users (
                        id SERIAL PRIMARY KEY,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS snow_gifts (
                        id SERIAL PRIMARY KEY,
                        gift_number INTEGER UNIQUE NOT NULL,
                        message TEXT NOT NULL,
                        gift_image TEXT NOT NULL,
                        box_image TEXT NOT NULL,
                        requires_auth BOOLEAN DEFAULT FALSE
                    );
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS snow_user_gifts (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER,
                        session_id TEXT NOT NULL,
                        gift_id INTEGER NOT NULL,
                        opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES snow_users(id) ON DELETE CASCADE
                    );
                """)
            else:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS snow_users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password_hash TEXT NOT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS snow_gifts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        gift_number INTEGER UNIQUE NOT NULL,
                        message TEXT NOT NULL,
                        gift_image TEXT NOT NULL,
                        box_image TEXT NOT NULL,
                        requires_auth BOOLEAN DEFAULT 0
                    );
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS snow_user_gifts (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        session_id TEXT NOT NULL,
                        gift_id INTEGER NOT NULL,
                        opened_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES snow_users(id) ON DELETE CASCADE
                    );
                """)
            
            conn.commit()
            print("Tables created successfully")
        except Exception as e:
            conn.rollback()
            print(f"Error creating tables: {e}")
        finally:
            conn.close()

    def init_gifts(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            # Проверяем есть ли уже подарки
            cursor.execute("SELECT COUNT(*) FROM snow_gifts")
            count = cursor.fetchone()[0]
            
            if count == 0:
                gifts = [
                    (1, "С Новым годом! Пусть сбудутся все мечты!", "gift1.jpg", "box.jpg", False),
                    (2, "Желаю здоровья, счастья и удачи в новом году!", "gift2.jpg", "box.jpg", False),
                    (3, "Пусть новый год принесет много радостных моментов!", "gift3.jpg", "box.jpg", True),
                    (4, "Счастья, любви и процветания в новом году!", "gift4.jpg", "box.jpg", False),
                    (5, "Мечтай, дерзай, достигай! С Новым годом!", "gift5.jpg", "box.jpg", False),
                    (6, "Пусть ангел-хранитель оберегает тебя весь год!", "gift6.jpg", "box.jpg", True),
                    (7, "Новых достижений и ярких впечатлений!", "gift7.jpg", "box.jpg", False),
                    (8, "Пусть каждый день будет наполнен счастьем!", "gift8.jpg", "box.jpg", False),
                    (9, "Успехов во всех начинаниях! С Новым годом!", "gift9.jpg", "box.jpg", True),
                    (10, "Гармонии, уюта и семейного тепла!", "gift10.jpg", "box.jpg", False)
                ]
                
                # Вставляем подарки
                if self.db.db_type == 'postgres':
                    for gift_number, message, gift_image, box_image, requires_auth in gifts:
                        cursor.execute(
                            """INSERT INTO snow_gifts 
                               (gift_number, message, gift_image, box_image, requires_auth) 
                               VALUES (%s, %s, %s, %s, %s)""",
                            (gift_number, message, gift_image, box_image, requires_auth)
                        )
                else:
                    for gift_number, message, gift_image, box_image, requires_auth in gifts:
                        cursor.execute(
                            """INSERT INTO snow_gifts 
                               (gift_number, message, gift_image, box_image, requires_auth) 
                               VALUES (?, ?, ?, ?, ?)""",
                            (gift_number, message, gift_image, box_image, 1 if requires_auth else 0)
                        )
                
                conn.commit()
                print(f"Initialized {len(gifts)} gifts")
            else:
                print(f"Gifts already exist: {count} gifts in database")
        except Exception as e:
            conn.rollback()
            print(f"Error initializing gifts: {e}")
        finally:
            conn.close()
    
    def get_all_gifts(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT * FROM snow_gifts ORDER BY gift_number")
            
            if self.db.db_type == 'postgres':
                columns = [desc[0] for desc in cursor.description]
                gifts = []
                for row in cursor.fetchall():
                    gift = dict(zip(columns, row))
                    if 'requires_auth' in gift:
                        gift['requires_auth'] = bool(gift['requires_auth'])
                    gifts.append(gift)
            else:
                gifts = [dict(gift) for gift in cursor.fetchall()]
            
            return gifts
        except Exception as e:
            print(f"Error getting gifts: {e}")
            return []
        finally:
            conn.close()
    
    def get_gift(self, gift_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.db.db_type == 'postgres':
                cursor.execute("SELECT * FROM snow_gifts WHERE id = %s", (gift_id,))
                columns = [desc[0] for desc in cursor.description]
                row = cursor.fetchone()
                if row:
                    gift = dict(zip(columns, row))
                    if 'requires_auth' in gift:
                        gift['requires_auth'] = bool(gift['requires_auth'])
                else:
                    gift = None
            else:
                cursor.execute("SELECT * FROM snow_gifts WHERE id = ?", (gift_id,))
                row = cursor.fetchone()
                gift = dict(row) if row else None
            
            return gift
        except Exception as e:
            print(f"Error getting gift: {e}")
            return None
        finally:
            conn.close()
    
    def reset_all_gifts(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute("DELETE FROM snow_user_gifts")
            conn.commit()
            print("All gifts reset successfully")
        except Exception as e:
            conn.rollback()
            print(f"Error resetting gifts: {e}")
        finally:
            conn.close()

class UserGiftModel:
    def __init__(self, db):
        self.db = db
    
    def add_opened_gift(self, user_id, session_id, gift_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            if self.db.db_type == 'postgres':
                cursor.execute(
                    """INSERT INTO snow_user_gifts (user_id, session_id, gift_id) 
                       VALUES (%s, %s, %s)""",
                    (user_id, session_id, gift_id)
                )
            else:
                cursor.execute(
                    """INSERT INTO snow_user_gifts (user_id, session_id, gift_id) 
                       VALUES (?, ?, ?)""",
                    (user_id, session_id, gift_id)
                )
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error adding opened gift: {e}")
            return False
        finally:
            conn.close()
    
    def get_opened_gifts_count(self, user_id=None, session_id=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            if user_id:
                if self.db.db_type == 'postgres':
                    cursor.execute(
                        "SELECT COUNT(*) FROM snow_user_gifts WHERE user_id = %s",
                        (user_id,)
                    )
                else:
                    cursor.execute(
                        "SELECT COUNT(*) FROM snow_user_gifts WHERE user_id = ?",
                        (user_id,)
                    )
            else:
                if self.db.db_type == 'postgres':
                    cursor.execute(
                        "SELECT COUNT(*) FROM snow_user_gifts WHERE session_id = %s",
                        (session_id,)
                    )
                else:
                    cursor.execute(
                        "SELECT COUNT(*) FROM snow_user_gifts WHERE session_id = ?",
                        (session_id,)
                    )
            
            count = cursor.fetchone()[0]
            return count
        except Exception as e:
            print(f"Error getting opened gifts count: {e}")
            return 0
        finally:
            conn.close()
    
    def get_opened_gifts(self, user_id=None, session_id=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            if user_id:
                if self.db.db_type == 'postgres':
                    cursor.execute(
                        """SELECT gift_id FROM snow_user_gifts 
                           WHERE user_id = %s""",
                        (user_id,)
                    )
                else:
                    cursor.execute(
                        """SELECT gift_id FROM snow_user_gifts 
                           WHERE user_id = ?""",
                        (user_id,)
                    )
            else:
                if self.db.db_type == 'postgres':
                    cursor.execute(
                        """SELECT gift_id FROM snow_user_gifts 
                           WHERE session_id = %s""",
                        (session_id,)
                    )
                else:
                    cursor.execute(
                        """SELECT gift_id FROM snow_user_gifts 
                           WHERE session_id = ?""",
                        (session_id,)
                    )
            
            if self.db.db_type == 'postgres':
                gifts = [row[0] for row in cursor.fetchall()]
            else:
                gifts = [gift[0] for gift in cursor.fetchall()]
            
            return gifts
        except Exception as e:
            print(f"Error getting opened gifts: {e}")
            return []
        finally:
            conn.close()
    
    def clear_user_gifts(self, user_id=None, session_id=None):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        
        try:
            if user_id:
                if self.db.db_type == 'postgres':
                    cursor.execute(
                        "DELETE FROM snow_user_gifts WHERE user_id = %s",
                        (user_id,)
                    )
                else:
                    cursor.execute(
                        "DELETE FROM snow_user_gifts WHERE user_id = ?",
                        (user_id,)
                    )
            else:
                if self.db.db_type == 'postgres':
                    cursor.execute(
                        "DELETE FROM snow_user_gifts WHERE session_id = %s",
                        (session_id,)
                    )
                else:
                    cursor.execute(
                        "DELETE FROM snow_user_gifts WHERE session_id = ?",
                        (session_id,)
                    )
            
            conn.commit()
            return True
        except Exception as e:
            conn.rollback()
            print(f"Error clearing user gifts: {e}")
            return False
        finally:
            conn.close()

db = Database()
user_model = UserModel(db)
gift_model = GiftModel(db)
user_gift_model = UserGiftModel(db)

tables_initialized = False

@lab9_bp.before_app_request
def initialize_database():
    global tables_initialized
    if not tables_initialized:
        # Создаем таблицы
        gift_model.create_tables()
        
        # Инициализируем подарки
        gift_model.init_gifts()
        
        tables_initialized = True

def generate_positions(count=10):
    fixed_positions = [
        {'left': '5%', 'top': '5%', 'width': '20%', 'height': '20%'},      
        {'left': '27%', 'top': '5%', 'width': '20%', 'height': '20%'},     
        {'left': '53%', 'top': '5%', 'width': '20%', 'height': '20%'},     
        {'left': '75%', 'top': '5%', 'width': '20%', 'height': '20%'},    
        
        {'left': '15%', 'top': '35%', 'width': '20%', 'height': '20%'},    
        {'left': '40%', 'top': '35%', 'width': '20%', 'height': '20%'},    
        {'left': '65%', 'top': '35%', 'width': '20%', 'height': '20%'},    
        
        {'left': '5%', 'top': '65%', 'width': '20%', 'height': '20%'},     
        {'left': '27%', 'top': '65%', 'width': '20%', 'height': '20%'},   
        {'left': '53%', 'top': '65%', 'width': '20%', 'height': '20%'},   
        {'left': '75%', 'top': '65%', 'width': '20%', 'height': '20%'},    
    ]
    
    return fixed_positions[:count]

@lab9_bp.route('/')
def main():
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()
    
    positions = generate_positions()
    gifts = gift_model.get_all_gifts()
    
    opened_gift_ids = []
    if 'user_id' in session:
        opened_gift_ids = user_gift_model.get_opened_gifts(
            user_id=session.get('user_id')
        )
    else:
        opened_gift_ids = user_gift_model.get_opened_gifts(
            session_id=session.get('session_id')
        )
    
    available_gifts = 10 - len(opened_gift_ids)
    
    return render_template('lab9/index.html', 
                         positions=positions,
                         gifts=gifts,
                         opened_gift_ids=opened_gift_ids,
                         available_gifts=available_gifts)

@lab9_bp.route('/open', methods=['POST'])
def open_gift():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    gift_id = data.get('gift_id')
    
    if not gift_id:
        return jsonify({'error': 'Gift ID is required'}), 400
    
    gift = gift_model.get_gift(gift_id)
    if not gift:
        return jsonify({'error': 'Подарок не найден'}), 404
    
    # Проверка авторизации для подарков требующих авторизации
    if gift['requires_auth'] and 'user_id' not in session:
        return jsonify({'error': 'Требуется авторизация для этого подарка'}), 403
    
    # Проверка количества открытых подарков
    opened_count = 0
    if 'user_id' in session:
        opened_count = user_gift_model.get_opened_gifts_count(
            user_id=session.get('user_id')
        )
    else:
        opened_count = user_gift_model.get_opened_gifts_count(
            session_id=session.get('session_id')
        )
    
    if opened_count >= 3:
        return jsonify({'error': 'Вы уже открыли максимальное количество подарков (3)'}), 403
    
    # Проверка, не открыт ли уже этот подарок
    opened_gift_ids = []
    if 'user_id' in session:
        opened_gift_ids = user_gift_model.get_opened_gifts(
            user_id=session.get('user_id')
        )
    else:
        opened_gift_ids = user_gift_model.get_opened_gifts(
            session_id=session.get('session_id')
        )
    
    if gift_id in opened_gift_ids:
        return jsonify({'error': 'Этот подарок уже открыт'}), 400
    
    # Добавляем запись об открытии подарка
    success = user_gift_model.add_opened_gift(
        session.get('user_id') if 'user_id' in session else None,
        session.get('session_id'),
        gift_id
    )
    
    if not success:
        return jsonify({'error': 'Ошибка при открытии подарка'}), 500
    
    available_gifts = 10 - (opened_count + 1)
    
    return jsonify({
        'success': True,
        'message': gift['message'],
        'gift_image': gift['gift_image'],
        'available_gifts': available_gifts
    })

@lab9_bp.route('/reset', methods=['POST'])
def reset_gifts():
    if 'user_id' not in session:
        return jsonify({'error': 'Требуется авторизация'}), 403
    
    try:
        gift_model.reset_all_gifts()
        
        # Очищаем пользовательские подарки
        if 'user_id' in session:
            user_gift_model.clear_user_gifts(user_id=session.get('user_id'))
        
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error resetting gifts: {e}")
        return jsonify({'error': 'Ошибка при сбросе подарков'}), 500

@lab9_bp.route('/enter', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_name = request.form.get('login')
        password = request.form.get('password')
        
        if not login_name or not password:
            return render_template('lab9/login.html', error='Заполните все поля')
        
        user = user_model.get_user_by_username(login_name)
        if user and user_model.check_password(user, password):
            session['user_id'] = user['id']
            session['user'] = login_name
            return redirect(url_for('lab9.main'))
        else:
            return render_template('lab9/login.html', error='Неверный логин или пароль')
    
    return render_template('lab9/login.html')

@lab9_bp.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login_name = request.form.get('login')
        password = request.form.get('password')
        
        if not login_name or not password:
            return render_template('lab9/register.html', error='Заполните все поля')
        
        if user_model.create_user(login_name, password):
            return redirect(url_for('lab9.login'))
        else:
            return render_template('lab9/register.html', error='Пользователь уже существует')
    
    return render_template('lab9/register.html')

@lab9_bp.route('/exit')
def logout():
    session.pop('user_id', None)
    session.pop('user', None)
    return redirect(url_for('lab9.main'))