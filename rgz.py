import re
from flask import Blueprint, jsonify, render_template, request, session, redirect, current_app
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
from psycopg2.extras import RealDictCursor
import sqlite3
from os import path

rgz = Blueprint('rgz', __name__)

def db_connect():
    try:
        if current_app.config['DB_TYPE'] == 'postgres':
            conn = psycopg2.connect(
                host='127.0.0.1',
                database='anastasia_agafonova_knowledge_base',
                user='anastasia_agafonova_knowledge_base',
                password='123',
                connect_timeout=10
            )
            cur = conn.cursor(cursor_factory=RealDictCursor)
        else:
            dir_path = path.dirname(path.realpath(__file__))
            db_path = path.join(dir_path, "database.db")
            conn = sqlite3.connect(db_path, timeout=10)
            conn.execute("PRAGMA foreign_keys = ON")
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
        
        return conn, cur
    except Exception as e:
        current_app.logger.error(f"Database connection error: {e}")
        raise

def db_close(conn, cur):
    try:
        conn.commit()
    except:
        pass
    finally:
        cur.close()
        conn.close()

def db_execute(query, params=None):
    """Универсальная функция выполнения SQL запросов"""
    conn, cur = db_connect()
    try:
        # Выполняем запрос
        if params:
            if isinstance(params, (list, tuple)):
                cur.execute(query, params)
            else:
                cur.execute(query, (params,))
        else:
            cur.execute(query)
        
        # Определяем тип запроса и возвращаем результат
        query_upper = query.strip().upper()
        
        if query_upper.startswith('INSERT'):
            conn.commit()
            # Получаем ID новой записи
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT LASTVAL()")
            else:
                cur.execute("SELECT last_insert_rowid()")
            result = cur.fetchone()[0]
            
        elif query_upper.startswith(('SELECT', 'WITH')):
            result = cur.fetchall()
            
        elif query_upper.startswith('UPDATE'):
            conn.commit()
            result = cur.rowcount  # Количество обновленных строк
            
        elif query_upper.startswith('DELETE'):
            conn.commit()
            result = cur.rowcount  # Количество удаленных строк
            
        else:
            conn.commit()
            result = None
            
        return result
        
    except Exception as e:
        conn.rollback()
        current_app.logger.error(f"Query error: {e}, Query: {query}, Params: {params}")
        raise e
        
    finally:
        db_close(conn, cur)

@rgz.route('/rgz/')
def main():
    conn, cur = db_connect()
    cur.execute("SELECT * FROM rgz_furniture")
    furniture = cur.fetchall()
    db_close(conn, cur)
    
    furniture_list = []
    for item in furniture:
        if hasattr(item, 'keys'):  
            furniture_list.append(dict(item))
        else:  
            furniture_list.append({
                'id': item[0],
                'name': item[1],
                'price': item[2],
                'description': item[3],
                'category': item[4],
                'image': item[5],
                'quantity': item[6]
            })
    
    return render_template('rgz/rgz.html', 
                         furniture_items=furniture_list,  
                         login=session.get('login'))

@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('rgz/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    # Валидация
    is_valid_login, login_error = validate_latin_chars(login)
    is_valid_password, password_error = validate_latin_chars(password)
    
    if not (is_valid_login and is_valid_password and login and password):
        error = login_error or password_error or 'Заполните все поля'
        return render_template('rgz/register.html', error=error)
    
    # Проверка существующего пользователя
    existing = db_execute("SELECT * FROM rgz_users WHERE login=?", (login,))
    if existing:
        return render_template('rgz/register.html', error='Пользователь уже существует')
    
    # Регистрация
    password_hash = generate_password_hash(password)
    db_execute("INSERT INTO rgz_users (login, password) VALUES (?, ?)", (login, password_hash))
    return render_template('rgz/success.html', login=login)

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    # Валидация
    is_valid_login, login_error = validate_latin_chars(login)
    is_valid_password, password_error = validate_latin_chars(password)
    
    if not (is_valid_login and is_valid_password and login and password):
        error = login_error or password_error or 'Заполните все поля'
        return render_template('rgz/login.html', error=error)
    
    # Проверка пользователя
    user = db_execute("SELECT * FROM rgz_users WHERE login=?", (login,))
    
    if not user or not check_password_hash(user[0]['password'], password):
        return render_template('rgz/login.html', error='Неверный логин или пароль')
    
    session['login'] = login
    session['user_id'] = user[0]['id']
    return redirect('/rgz/')

@rgz.route('/rgz/logout')
def logout():
    session.clear()
    return redirect('/rgz/')

@rgz.route('/rgz/cart')
def cart():
    return render_template('rgz/cart.html')

@rgz.route('/rgz/api', methods=['POST'])
def api():
    data = request.get_json()
    if not data or data.get('jsonrpc') != '2.0' or 'method' not in data:
        return json_rpc_error(-32600, "Invalid Request", data.get('id'))
    
    method = data.get('method')
    params = data.get('params', {})
    request_id = data.get('id')
    
    # Словарь методов для компактности
    methods = {
        'get_furniture': get_furniture,
        'add_to_cart': add_to_cart,
        'get_cart': get_cart,
        'remove_from_cart': remove_from_cart,
        'create_order': create_order,
        'delete_account': delete_account
    }
    
    handler = methods.get(method)
    if not handler:
        return json_rpc_error(-32601, "Method not found", request_id)
    
    return handler(params, request_id)

def json_rpc_response(result=None, error=None, request_id=None):
    response = {"jsonrpc": "2.0", "id": request_id}
    response["error" if error else "result"] = error or result
    return jsonify(response)

def json_rpc_error(code, message, request_id):
    return json_rpc_response(error={"code": code, "message": message}, request_id=request_id)

def require_auth(request_id):
    if not session.get('login'):
        return json_rpc_error(1, "Необходима авторизация", request_id)
    return session.get('user_id')

def get_furniture(params, request_id):
    furniture = db_execute("SELECT * FROM rgz_furniture ORDER BY name")
    return json_rpc_response([dict(item) for item in furniture], request_id=request_id)

def add_to_cart(params, request_id):
    user_id = require_auth(request_id)
    if isinstance(user_id, dict):
        return user_id
    
    furniture_id = params.get('furniture_id')
    if not furniture_id:
        return json_rpc_error(-32602, "Invalid params", request_id)
    
    # Проверка товара и его количества
    furniture = db_execute("SELECT * FROM rgz_furniture WHERE id=?", (furniture_id,))
    if not furniture:
        return json_rpc_error(2, "Товар не найден", request_id)
    
    # Проверяем, есть ли товар в наличии
    furniture_item = furniture[0]
    if furniture_item['quantity'] <= 0:
        return json_rpc_error(5, "Товар отсутствует на складе", request_id)
    
    # Проверка наличия в корзине
    existing = db_execute("SELECT * FROM rgz_cart WHERE user_id=? AND furniture_id=?", (user_id, furniture_id))
    
    if existing:
        # Проверяем, не превысим ли доступное количество
        cart_quantity = existing[0]['quantity'] + 1
        if cart_quantity > furniture_item['quantity']:
            return json_rpc_error(6, f"Недостаточно товара на складе. Доступно: {furniture_item['quantity']} шт.", request_id)
        
        db_execute("UPDATE rgz_cart SET quantity = quantity + 1 WHERE id=?", (existing[0]['id'],))
    else:
        db_execute("INSERT INTO rgz_cart (user_id, furniture_id, quantity) VALUES (?, ?, 1)", (user_id, furniture_id))
    
    db_execute("UPDATE rgz_furniture SET quantity = quantity - 1 WHERE id=?", (furniture_id,))
    
    return json_rpc_response({"success": True}, request_id=request_id)

def get_cart(params, request_id):
    user_id = require_auth(request_id)
    if isinstance(user_id, dict):
        return user_id
    
    cart_items = db_execute("""
        SELECT c.*, f.name, f.price, f.image 
        FROM rgz_cart c 
        JOIN rgz_furniture f ON c.furniture_id = f.id 
        WHERE c.user_id=?
    """, (user_id,))
    
    items = []
    total = 0
    for item in cart_items:
        item_dict = dict(item)
        item_total = float(item_dict['price']) * item_dict['quantity']
        item_dict['total'] = item_total
        total += item_total
        items.append(item_dict)
    
    return json_rpc_response({"items": items, "total": total}, request_id=request_id)

def remove_from_cart(params, request_id):
    user_id = require_auth(request_id)
    if isinstance(user_id, dict):
        return user_id
    
    cart_item_id = params.get('cart_item_id')
    if not cart_item_id:
        return json_rpc_error(-32602, "Invalid params", request_id)
    
    cart_item = db_execute("SELECT * FROM rgz_cart WHERE id=? AND user_id=?", (cart_item_id, user_id))
    if not cart_item:
        return json_rpc_error(3, "Товар не найден в корзине", request_id)
    
    furniture_id = cart_item[0]['furniture_id']
    quantity_to_remove = 1  # или cart_item[0]['quantity'] если удаляем все
    
    if cart_item[0]['quantity'] > 1:
        db_execute("UPDATE rgz_cart SET quantity = quantity - 1 WHERE id=?", (cart_item_id,))
    else:
        db_execute("DELETE FROM rgz_cart WHERE id=?", (cart_item_id,))
    
    db_execute("UPDATE rgz_furniture SET quantity = quantity + 1 WHERE id=?", (furniture_id,))
    
    return json_rpc_response({"success": True}, request_id=request_id)

def create_order(params, request_id):
    user_id = require_auth(request_id)
    if isinstance(user_id, dict):
        return user_id
    
    cart_items = db_execute("""
        SELECT c.*, f.price, f.quantity as available_quantity 
        FROM rgz_cart c 
        JOIN rgz_furniture f ON c.furniture_id = f.id 
        WHERE c.user_id=?
    """, (user_id,))
    
    if not cart_items:
        return json_rpc_error(4, "Корзина пуста", request_id)
    
    # Проверяем наличие всех товаров перед созданием заказа
    for item in cart_items:
        if item['quantity'] > item['available_quantity']:
            return json_rpc_error(7, f"Товара '{item['name']}' недостаточно на складе", request_id)
    
    # Подсчет суммы
    total_amount = sum(float(item['price']) * item['quantity'] for item in cart_items)
    
    # Создание заказа
    order_id = db_execute("INSERT INTO rgz_orders (user_id, total_amount) VALUES (?, ?)", (user_id, total_amount))
    
    # Добавление элементов заказа И уменьшение остатков на складе
    for item in cart_items:
        db_execute("""
            INSERT INTO rgz_order_items (order_id, furniture_id, quantity, price) 
            VALUES (?, ?, ?, ?)
        """, (order_id, item['furniture_id'], item['quantity'], item['price']))
        
        # Уменьшаем количество на складе после оформления заказа
        db_execute("""
            UPDATE rgz_furniture 
            SET quantity = quantity - ? 
            WHERE id = ?
        """, (item['quantity'], item['furniture_id']))
    
    # Очистка корзины
    db_execute("DELETE FROM rgz_cart WHERE user_id=?", (user_id,))
    
    return json_rpc_response({"order_id": order_id, "total_amount": total_amount}, request_id=request_id)

def delete_account(params, request_id):
    user_id = require_auth(request_id)
    if isinstance(user_id, dict):
        return user_id
    
    # Удаление всех данных пользователя
    db_execute("DELETE FROM rgz_cart WHERE user_id=?", (user_id,))
    
    # Удаление заказов
    orders = db_execute("SELECT id FROM rgz_orders WHERE user_id=?", (user_id,))
    for order in orders:
        db_execute("DELETE FROM rgz_order_items WHERE order_id=?", (order['id'],))
    db_execute("DELETE FROM rgz_orders WHERE user_id=?", (user_id,))
    
    # Удаление пользователя
    db_execute("DELETE FROM rgz_users WHERE id=?", (user_id,))
    
    session.clear()
    return json_rpc_response({"success": True, "message": "Аккаунт успешно удален"}, request_id=request_id)