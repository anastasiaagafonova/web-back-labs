from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
import random
import os
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

lab9_bp = Blueprint('lab9', __name__, template_folder='templates', static_folder='static')

# Классы моделей
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

# Инициализация моделей
db = Database('anastasia_agafonova_knowledge_base.db')
user_model = UserModel(db)
gift_model = GiftModel(db)
user_gift_model = UserGiftModel(db)

# Инициализируем подарки при первом запросе
gifts_initialized = False

@lab9_bp.before_app_request
def initialize():
    global gifts_initialized
    if not gifts_initialized:
        gift_model.init_gifts()
        gifts_initialized = True

# Генерация фиксированных случайных позиций
def generate_positions(count=10):
    positions = []
    random.seed(42)
    
    for i in range(count):
        left = random.randint(5, 85)
        top = random.randint(10, 80)
        positions.append({
            'id': i + 1,
            'left': f"{left}%",
            'top': f"{top}%"
        })
    
    return positions

# Главная страница
@lab9_bp.route('/')
def main():
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()
    
    positions = generate_positions()
    gifts = gift_model.get_all_gifts()
    
    # Получаем открытые подарки
    opened_gift_ids = []
    if 'user_id' in session:
        opened_gift_ids = user_gift_model.get_opened_gifts(
            user_id=session['user_id']
        )
    else:
        opened_gift_ids = user_gift_model.get_opened_gifts(
            session_id=session['session_id']
        )
    
    # Считаем доступные подарки
    available_gifts = 10 - len(opened_gift_ids)
    
    return render_template('lab9/index.html', 
                         positions=positions,
                         gifts=gifts,
                         opened_gift_ids=opened_gift_ids,
                         available_gifts=available_gifts,
                         login=session.get('user'))

# Открыть подарок
@lab9_bp.route('/open', methods=['POST'])
def open_gift():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    gift_id = data.get('gift_id')
    
    # Проверяем подарок
    gift = gift_model.get_gift(gift_id)
    if not gift:
        return jsonify({'error': 'Подарок не найден'}), 404
    
    # Проверяем авторизацию
    if gift['requires_auth'] and 'user_id' not in session:
        return jsonify({'error': 'Требуется авторизация для этого подарка'}), 403
    
    # Считаем открытые подарки
    opened_count = 0
    if 'user_id' in session:
        opened_count = user_gift_model.get_opened_gifts_count(
            user_id=session['user_id']
        )
    else:
        opened_count = user_gift_model.get_opened_gifts_count(
            session_id=session['session_id']
        )
    
    # Проверяем лимит
    if opened_count >= 3:
        return jsonify({'error': 'Вы уже открыли максимальное количество подарков (3)'}), 403
    
    # Проверяем, не открыт ли уже
    opened_gift_ids = []
    if 'user_id' in session:
        opened_gift_ids = user_gift_model.get_opened_gifts(
            user_id=session['user_id']
        )
    else:
        opened_gift_ids = user_gift_model.get_opened_gifts(
            session_id=session['session_id']
        )
    
    if gift_id in opened_gift_ids:
        return jsonify({'error': 'Этот подарок уже открыт'}), 400
    
    # Открываем подарок
    if 'user_id' in session:
        user_gift_model.add_opened_gift(
            session['user_id'], 
            session['session_id'], 
            gift_id
        )
    else:
        user_gift_model.add_opened_gift(
            None, 
            session['session_id'], 
            gift_id
        )
    
    gift_model.mark_as_opened(gift_id)
    
    # Считаем оставшиеся
    available_gifts = 10 - (opened_count + 1)
    
    return jsonify({
        'success': True,
        'message': gift['message'],
        'gift_image': gift['gift_image'],
        'available_gifts': available_gifts
    })

# Сбросить все подарки (Дед Мороз)
@lab9_bp.route('/reset', methods=['POST'])
def reset_gifts():
    if 'user_id' not in session:
        return jsonify({'error': 'Требуется авторизация'}), 403
    
    gift_model.reset_all_gifts()
    
    if 'user_id' in session:
        user_gift_model.clear_user_gifts(user_id=session['user_id'])
    if 'session_id' in session:
        user_gift_model.clear_user_gifts(session_id=session['session_id'])
    
    return jsonify({'success': True})

# Вход
@lab9_bp.route('/enter', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
        if not login or not password:
            return render_template('lab9/login.html', error='Заполните все поля')
        
        user = user_model.get_user_by_username(login)
        if user and user_model.check_password(user, password):
            session['user_id'] = user['id']
            session['user'] = login
            return redirect(url_for('lab9.main'))
        else:
            return render_template('lab9/login.html', error='Неверный логин или пароль')
    
    return render_template('lab9/login.html')

# Регистрация
@lab9_bp.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
        if not login or not password:
            return render_template('lab9/register.html', error='Заполните все поля')
        
        if user_model.create_user(login, password):
            return redirect(url_for('lab9.login'))
        else:
            return render_template('lab9/register.html', error='Пользователь уже существует')
    
    return render_template('lab9/register.html')

# Выход
@lab9_bp.route('/exit')
def logout():
    session.pop('user_id', None)
    session.pop('user', None)
    return redirect(url_for('lab9.main'))