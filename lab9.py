lab9.py
from flask import Blueprint, render_template, session, jsonify, request, current_app, redirect, url_for
import random
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

lab9 = Blueprint('lab9', __name__)

def db_connect():
    if current_app.config.get('DB_TYPE') == 'postgres':
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='anastasia_agafonova_gift',
            user='anastasia_agafonova_gift',
            password='1234567'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def is_authenticated():
    return session.get('user_authenticated', False)


def get_user_id():
    if 'lab9_user_id' not in session:
        session['lab9_user_id'] = str(uuid.uuid4())
    return session['lab9_user_id']

def generate_positions():
    positions = []
    box_width = 10   
    box_height = 12  
    
    for _ in range(10):
        while True:
            top = random.randint(5, 85 - box_height)
            left = random.randint(5, 85 - box_width)
            
            # проверка пересечений
            overlap = False
            for (t, l) in positions:
                if (abs(top - t) < box_height and abs(left - l) < box_width):
                    overlap = True
                    break
            
            if not overlap:
                positions.append((top, left))
                break
    
    return positions

def init_user_gifts(user_id, cur):
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT COUNT(*) as cnt FROM lab9_gifts WHERE user_id = %s", (user_id,))
    else:
        cur.execute("SELECT COUNT(*) as cnt FROM lab9_gifts WHERE user_id = ?", (user_id,))
    
    if cur.fetchone()['cnt'] > 0:
        return False 
    
    # ПЕРЕМЕСТИЛИ ВНУТРЬ ФУНКЦИИ!
    congratulations = [
        "С Новым Годом! Пусть мечты сбываются, а счастье не кончается!",
        "Пусть новый год принесёт здоровье, удачу и благополучие!",
        "Желаю ярких впечатлений, интересных событий и верных друзей!",
        "Пусть каждый день будет наполнен радостью и вдохновением!",
        "Желаю успехов во всех начинаниях и крепкого здоровья!",
        "Пусть сбудутся самые заветные желания под бой курантов!",
        "Желаю тепла в доме, уюта в сердце и мира в душе!",
        "Пусть новый год будет полон счастливых моментов и приятных сюрпризов!",
        "Желаю финансового благополучия и карьерного роста!",
        "Пусть этот год станет самым лучшим в вашей жизни!"
    ]
    
    gift_images = [f"gift{i+1}.jpg" for i in range(10)]
    box_images = [f"box{i+1}.jpg" for i in range(10)]

    positions = generate_positions()

    for i in range(10):
        top_pos, left_pos = positions[i]
        require_auth = (i >= 5)  # Последние 5 подарков требуют авторизации
        
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("""
                INSERT INTO lab9_gifts 
                (user_id, position_id, top_position, left_position, message, image, box_image, require_auth)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, i, top_pos, left_pos, congratulations[i], gift_images[i], box_images[i], require_auth))
        else:
            cur.execute("""
                INSERT INTO lab9_gifts 
                (user_id, position_id, top_position, left_position, message, image, box_image, require_auth)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (user_id, i, top_pos, left_pos, congratulations[i], gift_images[i], box_images[i], require_auth))
    
    return True

@lab9.route('/lab9/')
def main():
    conn, cur = db_connect()
    
    # Получаем ID пользователя
    user_id = get_user_id()
    
    # Создаём запись пользователя если нет
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT id FROM lab9_users WHERE id = %s", (user_id,))
    else:
        cur.execute("SELECT id FROM lab9_users WHERE id = ?", (user_id,))
    
    if not cur.fetchone():
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("INSERT INTO lab9_users (id) VALUES (%s)", (user_id,))
        else:
            cur.execute("INSERT INTO lab9_users (id) VALUES (?)", (user_id,))
    
    # Инициализируем подарки если нужно
    init_user_gifts(user_id, cur)
    
    # получаем подарки пользователя
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("""
            SELECT position_id, top_position, left_position, opened, 
                   message, image, box_image, require_auth 
            FROM lab9_gifts 
            WHERE user_id = %s 
            ORDER BY position_id
        """, (user_id,))
    else:
        cur.execute("""
            SELECT position_id, top_position, left_position, opened, 
                   message, image, box_image, require_auth 
            FROM lab9_gifts 
            WHERE user_id = ? 
            ORDER BY position_id
        """, (user_id,))
    
    gifts = cur.fetchall()
    
    # считаем открытые подарки
    if current_app.config.get('DB_TYPE') == 'postgres':
        cur.execute("SELECT COUNT(*) as cnt FROM lab9_gifts WHERE user_id = %s AND opened = TRUE", (user_id,))
    else:
        cur.execute("SELECT COUNT(*) as cnt FROM lab9_gifts WHERE user_id = ? AND opened = 1", (user_id,))
    
    opened_count = cur.fetchone()['cnt']
    
    db_close(conn, cur)
    
    return render_template('lab9/index.html',
                         gifts=gifts,
                         opened_count=opened_count,
                         remaining=10 - opened_count,
                         is_auth=is_authenticated(),
                         login=session.get('login'))

@lab9.route('/lab9/open_gift', methods=['POST'])
def open_gift():
    user_id = get_user_id()
    data = request.json
    gift_id = data.get('gift_id')
    
    if not gift_id or gift_id not in range(10):
        return jsonify({'success': False, 'message': 'Неверный ID подарка'})
    
    conn, cur = db_connect()
    
    try:
        # получаем информацию о подарке
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("""
                SELECT require_auth, opened, message, image 
                FROM lab9_gifts 
                WHERE user_id = %s AND position_id = %s
            """, (user_id, gift_id))
        else:
            cur.execute("""
                SELECT require_auth, opened, message, image 
                FROM lab9_gifts 
                WHERE user_id = ? AND position_id = ?
            """, (user_id, gift_id))
        
        gift = cur.fetchone()
        
        if not gift:
            return jsonify({'success': False, 'message': 'Подарок не найден'})
        
        # проверяем, не открыт ли уже
        if gift['opened']:
            return jsonify({'success': False, 'message': 'Этот подарок уже открыт!'})
        
        # проверяем требование авторизации
        if gift['require_auth'] and not is_authenticated():
            return jsonify({
                'success': False,
                'message': 'Для открытия этого подарка требуется авторизация!'
            })
        
        # проверяем лимит открытых подарков 
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT COUNT(*) as cnt FROM lab9_gifts WHERE user_id = %s AND opened = TRUE", (user_id,))
        else:
            cur.execute("SELECT COUNT(*) as cnt FROM lab9_gifts WHERE user_id = ? AND opened = 1", (user_id,))
        
        opened_count = cur.fetchone()['cnt']
        
        if opened_count >= 3:
            return jsonify({
                'success': False,
                'message': 'Вы уже открыли максимальное количество подарков (3)!'
            })
        
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("""
                UPDATE lab9_gifts 
                SET opened = TRUE, opened_at = NOW()
                WHERE user_id = %s AND position_id = %s
                RETURNING message, image
            """, (user_id, gift_id))
        else:
            cur.execute("""
                UPDATE lab9_gifts 
                SET opened = 1, opened_at = ?
                WHERE user_id = ? AND position_id = ?
            """, (datetime.now(), user_id, gift_id))
            cur.execute("SELECT message, image FROM lab9_gifts WHERE user_id = ? AND position_id = ?", 
                       (user_id, gift_id))
        
        gift_data = cur.fetchone()
        new_opened_count = opened_count + 1
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': gift_data['message'],
            'image': gift_data['image'],
            'opened_count': new_opened_count,
            'remaining': 10 - new_opened_count
        })
        
    except Exception as e:
        print(f"Ошибка при открытии подарка: {e}")
        conn.rollback()
        return jsonify({'success': False, 'message': 'Ошибка сервера'})
    finally:
        db_close(conn, cur)

@lab9.route('/lab9/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab9/login.html')
    
    login_val = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()
    
    if not login_val or not password:
        return render_template('lab9/login.html', error='Заполните все поля')
    
    conn, cur = db_connect()
    
    try:
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id, password FROM lab9_auth_users WHERE login = %s", (login_val,))
        else:
            cur.execute("SELECT id, password FROM lab9_auth_users WHERE login = ?", (login_val,))
        
        user = cur.fetchone()
        
        if not user:
            return render_template('lab9/login.html', error='Неверный логин или пароль')
        
        if not check_password_hash(user['password'], password):
            return render_template('lab9/login.html', error='Неверный логин или пароль')
        
        session['user_authenticated'] = True
        session['login'] = login_val
        session['auth_user_id'] = user['id']
        
        return redirect('/lab9/')
        
    except Exception as e:
        print(f"Ошибка при входе: {e}")
        return render_template('lab9/login.html', error='Ошибка сервера')
    finally:
        db_close(conn, cur)

@lab9.route('/lab9/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab9/register.html')
    
    login_val = request.form.get('login', '').strip()
    password = request.form.get('password', '').strip()
    confirm_password = request.form.get('confirm_password', '').strip()
    
    errors = []
    if not login_val:
        errors.append('Введите логин')
    if not password:
        errors.append('Введите пароль')
    if password != confirm_password:
        errors.append('Пароли не совпадают')
    if len(password) < 4:
        errors.append('Пароль должен быть не менее 4 символов')
    
    if errors:
        return render_template('lab9/register.html', error='; '.join(errors))
    
    conn, cur = db_connect()
    
    try:
        # проверяем уникальность логина
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("SELECT id FROM lab9_auth_users WHERE login = %s", (login_val,))
        else:
            cur.execute("SELECT id FROM lab9_auth_users WHERE login = ?", (login_val,))
        
        if cur.fetchone():
            return render_template('lab9/register.html', error='Логин уже занят')
        
        # cоздаём пользователя
        password_hash = generate_password_hash(password)
        
        if current_app.config.get('DB_TYPE') == 'postgres':
            cur.execute("INSERT INTO lab9_auth_users (login, password) VALUES (%s, %s) RETURNING id", 
                       (login_val, password_hash))
            user_id = cur.fetchone()['id']
        else:
            cur.execute("INSERT INTO lab9_auth_users (login, password) VALUES (?, ?)", 
                       (login_val, password_hash))
            user_id = cur.lastrowid
        
        # Авторизуем пользователя
        session['user_authenticated'] = True
        session['login'] = login_val
        session['auth_user_id'] = user_id
        
        conn.commit()
        return redirect('/lab9/')
        
    except Exception as e:
        print(f"Ошибка при регистрации: {e}")
        conn.rollback()
        return render_template('lab9/register.html', error='Ошибка регистрации')
    finally:
        db_close(conn, cur)

@lab9.route('/lab9/logout')
def logout():
    """Выход из системы"""
    session.pop('user_authenticated', None)
    session.pop('login', None)
    session.pop('auth_user_id', None)
    return redirect('/lab9/')

@lab9.route('/lab9/reset_gifts', methods=['POST'])
def reset_gifts():
    """Сброс всех подарков (только для авторизованных)"""
    if not is_authenticated():
        return jsonify({'success': False, 'message': 'Требуется авторизация'})
    
    user_id = get_user_id()
    conn, cur = db_connect()
    
    try:
        # Генерируем новые позиции
        positions = generate_positions()
        
        # Сбрасываем все подарки
        for i in range(10):
            top_pos, left_pos = positions[i]
            
            if current_app.config.get('DB_TYPE') == 'postgres':
                cur.execute("""
                    UPDATE lab9_gifts 
                    SET opened = FALSE, opened_at = NULL,
                        top_position = %s, left_position = %s
                    WHERE user_id = %s AND position_id = %s
                """, (top_pos, left_pos, user_id, i))
            else:
                cur.execute("""
                    UPDATE lab9_gifts 
                    SET opened = 0, opened_at = NULL,
                        top_position = ?, left_position = ?
                    WHERE user_id = ? AND position_id = ?
                """, (top_pos, left_pos, user_id, i))
        
        conn.commit()
        
        return jsonify({
            'success': True,
            'message': '🎅 Дед Мороз обновил подарки! Все коробки снова закрыты!'
        })
        
    except Exception as e:
        print(f"Ошибка при сбросе: {e}")
        conn.rollback()
        return jsonify({'success': False, 'message': 'Ошибка сервера'})
    finally:
        db_close(conn, cur)