from flask import Blueprint, Flask, render_template, request, jsonify, session, redirect, url_for
from models import Database, UserModel, GiftModel, UserGiftModel
import random
import os

lab9 = Blueprint('lab9', __name__)

lab9.secret_key = 'your-secret-key-here-change-in-production'
lab9.config['DATABASE'] = 'anastasia_agafonova_knowledge_base.db'

# Инициализация моделей
db = Database(lab9.config['DATABASE'])
user_model = UserModel(db)
gift_model = GiftModel(db)
user_gift_model = UserGiftModel(db)

# Инициализация подарков при первом запуске
@lab9.before_first_request
def init_gifts():
    gift_model.init_gifts()

# Генерация фиксированных случайных позиций
def generate_positions(count=10):
    positions = []
    random.seed(42)  # Фиксируем seed для одинаковых позиций
    
    for i in range(count):
        left = random.randint(5, 85)  # Проценты от ширины
        top = random.randint(10, 80)   # Проценты от высоты
        positions.lab9end({
            'id': i + 1,
            'left': f"{left}%",
            'top': f"{top}%"
        })
    
    return positions

@lab9.route('/')
def index():
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
    
    return render_template('index.html', 
                         positions=positions,
                         gifts=gifts,
                         opened_gift_ids=opened_gift_ids,
                         available_gifts=available_gifts,
                         user=session.get('user'))

@lab9.route('/open_gift', methods=['POST'])
def open_gift():
    gift_id = request.json.get('gift_id')
    
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

@lab9.route('/reset_gifts', methods=['POST'])
def reset_gifts():
    if 'user_id' not in session:
        return jsonify({'error': 'Требуется авторизация'}), 403
    
    gift_model.reset_all_gifts()
    
    if 'user_id' in session:
        user_gift_model.clear_user_gifts(user_id=session['user_id'])
    if 'session_id' in session:
        user_gift_model.clear_user_gifts(session_id=session['session_id'])
    
    return jsonify({'success': True})

@lab9.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if user_model.create_user(username, password):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='Пользователь уже существует')
    
    return render_template('register.html')

@lab9.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = user_model.get_user_by_username(username)
        if user and user_model.check_password(user, password):
            session['user_id'] = user['id']
            session['user'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Неверные данные')
    
    return render_template('login.html')

@lab9.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    lab9.run(debug=True, port=5000)