from flask import Flask, Blueprint, render_template, request, jsonify, session, redirect, url_for
import random
import os
from lab9.models import Database, UserModel, GiftModel, UserGiftModel

lab9_bp = Blueprint('lab9', __name__, template_folder='templates', static_folder='static')

# Инициализация моделей
db = Database('anastasia_agafonova_knowledge_base.db')
user_model = UserModel(db)
gift_model = GiftModel(db)
user_gift_model = UserGiftModel(db)

# Инициализация подарков
def init_app():
    gift_model.init_gifts()

# Генерация фиксированных случайных позиций
def generate_positions(count=10):
    positions = []
    random.seed(42)  # Фиксируем seed для одинаковых позиций
    
    for i in range(count):
        left = random.randint(5, 85)  # Проценты от ширины
        top = random.randint(10, 80)   # Проценты от высоты
        positions.append({
            'id': i + 1,
            'left': f"{left}%",
            'top': f"{top}%"
        })
    
    return positions

@lab9_bp.route('/')
def main():
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()
    
    positions = generate_positions()
    gifts = gift_model.get_all_gifts()
    
    # Получаем открытые подарки для текущей сессии/пользователя
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

@lab9_bp.route('/open_gift', methods=['POST'])
def open_gift():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No JSON data provided'}), 400
    
    gift_id = data.get('gift_id')
    
    # Проверяем существование подарка
    gift = gift_model.get_gift(gift_id)
    if not gift:
        return jsonify({'error': 'Подарок не найден'}), 404
    
    # Проверяем авторизацию для специальных подарков
    if gift['requires_auth'] and 'user_id' not in session:
        return jsonify({'error': 'Требуется авторизация для этого подарка'}), 403
    
    # Получаем количество уже открытых подарков
    opened_count = 0
    if 'user_id' in session:
        opened_count = user_gift_model.get_opened_gifts_count(
            user_id=session['user_id']
        )
    else:
        opened_count = user_gift_model.get_opened_gifts_count(
            session_id=session['session_id']
        )
    
    # Проверяем лимит (максимум 3 подарка)
    if opened_count >= 3:
        return jsonify({'error': 'Вы уже открыли максимальное количество подарков (3)'}), 403
    
    # Проверяем, не открыт ли уже этот подарок
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
    
    # Считаем оставшиеся подарки
    available_gifts = 10 - (opened_count + 1)
    
    return jsonify({
        'success': True,
        'message': gift['message'],
        'gift_image': gift['gift_image'],
        'available_gifts': available_gifts
    })

@lab9_bp.route('/reset_gifts', methods=['POST'])
def reset_gifts():
    if 'user_id' not in session:
        return jsonify({'error': 'Требуется авторизация'}), 403
    
    gift_model.reset_all_gifts()
    
    if 'user_id' in session:
        user_gift_model.clear_user_gifts(user_id=session['user_id'])
    if 'session_id' in session:
        user_gift_model.clear_user_gifts(session_id=session['session_id'])
    
    return jsonify({'success': True})

@lab9_bp.route('/login', methods=['GET', 'POST'])
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

@lab9_bp.route('/register', methods=['GET', 'POST'])
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

@lab9_bp.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user', None)
    return redirect(url_for('lab9.main'))

# Инициализация при первом запросе
@lab9_bp.before_app_first_request
def initialize():
    init_app()