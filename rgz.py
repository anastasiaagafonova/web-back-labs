from flask import Blueprint, request, jsonify, session, current_app, render_template
import sqlite3
import json
from datetime import datetime
import hashlib
import secrets
import os
from pathlib import Path

rgz = Blueprint('rgz', __name__)

def db_connect():
    if current_app.config.get('DB_TYPE') == 'postgres':
        # Ваш существующий код для PostgreSQL
        import psycopg2
        from psycopg2.extras import RealDictCursor
        conn = psycopg2.connect(
            host='127.0.0.1',
            database='anastasia_agafonova_knowledge_base',
            user='anastasia_agafonova_knowledge_base',
            password='123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        # SQLite подключение
        dir_path = os.path.dirname(os.path.realpath(__file__))
        db_path = os.path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
    
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

def add_sample_furniture(cur):
    """Добавление тестовых товаров мебели"""
    furniture_data = [
        # Диваны
        ('Диван угловой "Комфорт"', 'Просторный угловой диван с ортопедическим матрасом', 45000.00, 'Диваны', '/static/lab6/images/sofa1.jpg', 10, 'Ткань', 'Серый', '220x160x90 см', 85.5),
        ('Диван прямой "Модерн"', 'Современный прямой диван с деревянными ножками', 32000.00, 'Диваны', '/static/lab6/images/sofa2.jpg', 8, 'Экокожа', 'Черный', '200x90x85 см', 65.0),
        ('Диван-кровать "Трансформер"', 'Удобный диван-кровать с механизмом трансформации', 38000.00, 'Диваны', '/static/lab6/images/sofa3.jpg', 5, 'Велюр', 'Бежевый', '190x140x90 см', 75.2),
        
        # Кресла
        ('Кресло офисное "Эргономик"', 'Эргономичное кресло с регулировкой высоты', 12000.00, 'Кресла', '/static/lab6/images/chair1.jpg', 15, 'Кожа', 'Черный', '65x65x110 см', 18.2),
        ('Кресло качалка "Классик"', 'Деревянное кресло-качалка для отдыха', 8500.00, 'Кресла', '/static/lab6/images/chair2.jpg', 12, 'Массив дерева', 'Коричневый', '70x90x100 см', 15.8),
        ('Кресло компьютерное "Геймер"', 'Игровое кресло с поддержкой спины', 15000.00, 'Кресла', '/static/lab6/images/chair3.jpg', 7, 'Ткань', 'Красный', '70x70x130 см', 25.5),
        
        # Столы
        ('Стол обеденный "Семейный"', 'Деревянный обеденный стол на 6 персон', 25000.00, 'Столы', '/static/lab6/images/table1.jpg', 8, 'Дуб', 'Натуральный', '160x90x75 см', 35.0),
        ('Стол письменный "Офис"', 'Большой письменный стол с ящиками', 18000.00, 'Столы', '/static/lab6/images/table2.jpg', 6, 'ЛДСП', 'Белый', '140x70x75 см', 28.5),
        ('Стол журнальный "Мини"', 'Небольшой журнальный столик', 7500.00, 'Столы', '/static/lab6/images/table3.jpg', 10, 'Стекло', 'Прозрачный', '80x50x45 см', 12.3),
        
        # Стулья
        ('Стул кухонный "Классик"', 'Комфортный стул для кухни или столовой', 3500.00, 'Стулья', '/static/lab6/images/chair4.jpg', 25, 'Бук', 'Бежевый', '45x45x85 см', 4.5),
        ('Стул офисный "Стандарт"', 'Офисный стул с мягким сиденьем', 4200.00, 'Стулья', '/static/lab6/images/chair5.jpg', 20, 'Пластик', 'Серый', '50x50x80 см', 5.2),
        ('Стул барный "Высокий"', 'Барный стул для кухонной стойки', 5800.00, 'Стулья', '/static/lab6/images/chair6.jpg', 8, 'Металл', 'Хром', '40x40x110 см', 6.8),
        
        # Кровати
        ('Кровать двуспальная "Рояль"', 'Двуспальная кровать с мягким изголовьем', 32000.00, 'Кровати', '/static/lab6/images/bed1.jpg', 6, 'Массив', 'Белый', '200x180 см', 45.8),
        ('Кровать односпальная "Мини"', 'Компактная односпальная кровать', 18500.00, 'Кровати', '/static/lab6/images/bed2.jpg', 10, 'ЛДСП', 'Венге', '200x90 см', 32.0),
        ('Кровать детская "Сказка"', 'Детская кровать с бортиками', 22000.00, 'Кровати', '/static/lab6/images/bed3.jpg', 4, 'Массив', 'Голубой', '160x80 см', 28.5),
        
        # Шкафы
        ('Шкаф-купе "Модерн"', 'Вместительный шкаф-купе с зеркальными дверями', 38000.00, 'Шкафы', '/static/lab6/images/wardrobe1.jpg', 4, 'ЛДСП', 'Венге', '240x60x220 см', 120.0),
        ('Шкаф распашной "Классика"', 'Распашной шкаф с деревянными дверями', 29500.00, 'Шкафы', '/static/lab6/images/wardrobe2.jpg', 5, 'Массив', 'Коричневый', '180x50x210 см', 95.5),
        ('Шкаф книжный "Библиотека"', 'Книжный шкаф с полками', 14200.00, 'Шкафы', '/static/lab6/images/wardrobe3.jpg', 7, 'ДСП', 'Белый', '120x35x200 см', 45.2),
        
        # Комоды
        ('Комод "Практик"', 'Вместительный комод с выдвижными ящиками', 12500.00, 'Комоды', '/static/lab6/images/chest1.jpg', 8, 'ЛДСП', 'Дуб', '100x45x85 см', 25.8),
        ('Комод прикроватный "Мини"', 'Небольшой комод для спальни', 8500.00, 'Комоды', '/static/lab6/images/chest2.jpg', 12, 'МДФ', 'Белый', '60x40x70 см', 15.3),
        
        # Тумбы
        ('Тумба ТВ "Современная"', 'Телевизионная тумба для техники', 11200.00, 'Тумбы', '/static/lab6/images/cabinet1.jpg', 6, 'Стекло', 'Черный', '120x40x50 см', 18.9),
        ('Тумба прикроватная "Ночка"', 'Прикроватная тумбочка', 4800.00, 'Тумбы', '/static/lab6/images/cabinet2.jpg', 15, 'Дерево', 'Светлый', '45x45x55 см', 8.2)
    ]
    
    for furniture in furniture_data:
        cur.execute('''
            INSERT INTO product (name, description, price, category, image_url, stock, material, color, dimensions, weight)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', furniture)

@rgz.route('/')
def index():
    # Проверяем и добавляем тестовые товары при необходимости
    conn, cur = db_connect()
    try:
        cur.execute("SELECT COUNT(*) FROM product")
        if cur.fetchone()[0] == 0:
            add_sample_furniture(cur)
    except Exception as e:
        print(f"Error checking products: {e}")
    finally:
        db_close(conn, cur)
    
    return render_template('lab6/index.html')

@rgz.route('/cart')
def cart():
    return render_template('lab6/cart.html')

# JSON-RPC API endpoints
@rgz.route('/api/user')
def get_user():
    if 'user_id' in session:
        return jsonify({
            'success': True,
            'user': {
                'id': session['user_id'],
                'login': session['login']
            }
        })
    return jsonify({'success': False})

@rgz.route('/api/products')
def get_products():
    conn, cur = db_connect()
    
    try:
        cur.execute('''
            SELECT * FROM product 
            WHERE stock > 0 
            ORDER BY created_at DESC
        ''')
        products = [dict(row) for row in cur.fetchall()]
        return jsonify({'success': True, 'products': products})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        db_close(conn, cur)

@rgz.route('/api/cart', methods=['GET', 'POST'])
def handle_cart():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'})
    
    conn, cur = db_connect()
    
    try:
        if request.method == 'GET':
            cur.execute('''
                SELECT c.*, p.name, p.price, p.image_url, p.stock 
                FROM cart c 
                JOIN product p ON c.product_id = p.id 
                WHERE c.user_id = ?
            ''', (session['user_id'],))
            cart_items = [dict(row) for row in cur.fetchall()]
            return jsonify({'success': True, 'cart': cart_items})
            
        elif request.method == 'POST':
            data = request.get_json()
            
            # JSON-RPC формат
            if 'method' in data:
                method = data['method']
                params = data.get('params', {})
                product_id = params.get('product_id')
                quantity = params.get('quantity', 1)
            else:
                # Простой формат
                product_id = data.get('product_id')
                quantity = data.get('quantity', 1)
            
            # Проверяем наличие товара
            cur.execute('SELECT * FROM product WHERE id = ? AND stock >= ?', (product_id, quantity))
            product = cur.fetchone()
            
            if not product:
                return jsonify({'success': False, 'error': 'Товар недоступен'})
            
            # Проверяем есть ли уже товар в корзине
            cur.execute('SELECT * FROM cart WHERE user_id = ? AND product_id = ?', 
                       (session['user_id'], product_id))
            existing = cur.fetchone()
            
            if existing:
                # Обновляем количество
                new_quantity = existing['quantity'] + quantity
                if new_quantity > product['stock']:
                    return jsonify({'success': False, 'error': 'Недостаточно товара на складе'})
                
                cur.execute('UPDATE cart SET quantity = ? WHERE id = ?', 
                           (new_quantity, existing['id']))
            else:
                # Добавляем новый товар
                cur.execute('INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)', 
                           (session['user_id'], product_id, quantity))
            
            return jsonify({
                'success': True, 
                'message': 'Product added to cart',
                'jsonrpc': '2.0',
                'id': data.get('id')
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        db_close(conn, cur)

@rgz.route('/api/cart/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'})
    
    conn, cur = db_connect()
    
    try:
        data = request.get_json() or {}
        
        cur.execute('DELETE FROM cart WHERE id = ? AND user_id = ?', 
                   (item_id, session['user_id']))
        
        if cur.rowcount == 0:
            return jsonify({
                'success': False, 
                'error': 'Item not found in cart',
                'jsonrpc': '2.0',
                'id': data.get('id')
            })
        
        return jsonify({
            'success': True, 
            'message': 'Item removed from cart',
            'jsonrpc': '2.0',
            'id': data.get('id')
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        db_close(conn, cur)

@rgz.route('/api/orders', methods=['POST'])
def create_order():
    if 'user_id' not in session:
        return jsonify({'success': False, 'error': 'Not authorized'})
    
    data = request.get_json()
    
    # JSON-RPC формат
    if 'method' in data:
        params = data.get('params', {})
        shipping_address = params.get('shipping_address', '')
        request_id = data.get('id')
    else:
        # Простой формат
        shipping_address = data.get('shipping_address', '')
        request_id = None
    
    if not shipping_address.strip():
        return jsonify({
            'success': False, 
            'error': 'Shipping address is required',
            'jsonrpc': '2.0',
            'id': request_id
        })
    
    conn, cur = db_connect()
    
    try:
        # Получаем товары из корзины
        cur.execute('''
            SELECT c.*, p.price, p.name, p.stock 
            FROM cart c 
            JOIN product p ON c.product_id = p.id 
            WHERE c.user_id = ?
        ''', (session['user_id'],))
        cart_items = cur.fetchall()
        
        if not cart_items:
            return jsonify({
                'success': False, 
                'error': 'Cart is empty',
                'jsonrpc': '2.0',
                'id': request_id
            })
        
        # Проверяем наличие товаров на складе
        for item in cart_items:
            if item['stock'] < item['quantity']:
                return jsonify({
                    'success': False, 
                    'error': f'Недостаточно товара "{item["name"]}" на складе',
                    'jsonrpc': '2.0',
                    'id': request_id
                })
        
        # Рассчитываем общую сумму
        total_amount = sum(float(item['price']) * item['quantity'] for item in cart_items)
        
        # Создаем заказ
        cur.execute('''
            INSERT INTO orders (user_id, total_amount, shipping_address) 
            VALUES (?, ?, ?)
        ''', (session['user_id'], total_amount, shipping_address))
        order_id = cur.lastrowid
        
        # Добавляем товары в заказ и обновляем склад
        for item in cart_items:
            cur.execute('''
                INSERT INTO order_item (order_id, product_id, quantity, price) 
                VALUES (?, ?, ?, ?)
            ''', (order_id, item['product_id'], item['quantity'], item['price']))
            
            # Обновляем количество на складе
            cur.execute('UPDATE product SET stock = stock - ? WHERE id = ?', 
                       (item['quantity'], item['product_id']))
        
        # Очищаем корзину
        cur.execute('DELETE FROM cart WHERE user_id = ?', (session['user_id'],))
        
        return jsonify({
            'success': True, 
            'order_id': order_id, 
            'total_amount': total_amount,
            'message': 'Order created successfully',
            'jsonrpc': '2.0',
            'id': request_id
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
    finally:
        db_close(conn, cur)

# Дополнительные API методы
@rgz.route('/json-rpc-api/', methods=['POST'])
def json_rpc_api():
    """Основной JSON-RPC endpoint"""
    data = request.get_json()
    
    if not data or 'method' not in data:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {'code': -32600, 'message': 'Invalid Request'},
            'id': None
        })
    
    method = data['method']
    params = data.get('params', {})
    request_id = data.get('id')
    
    if method == 'get_products':
        return get_products_json_rpc(request_id)
    elif method == 'add_to_cart':
        return add_to_cart_json_rpc(params, request_id)
    elif method == 'remove_from_cart':
        return remove_from_cart_json_rpc(params, request_id)
    elif method == 'create_order':
        return create_order_json_rpc(params, request_id)
    elif method == 'get_cart':
        return get_cart_json_rpc(request_id)
    else:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {'code': -32601, 'message': 'Method not found'},
            'id': request_id
        })

def get_products_json_rpc(request_id):
    conn, cur = db_connect()
    try:
        cur.execute('SELECT * FROM product WHERE stock > 0 ORDER BY created_at DESC')
        products = [dict(row) for row in cur.fetchall()]
        return jsonify({
            'jsonrpc': '2.0',
            'result': products,
            'id': request_id
        })
    except Exception as e:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {'code': -32000, 'message': str(e)},
            'id': request_id
        })
    finally:
        db_close(conn, cur)

def add_to_cart_json_rpc(params, request_id):
    if 'user_id' not in session:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {'code': 1, 'message': 'Not authorized'},
            'id': request_id
        })
    
    return handle_cart()

def remove_from_cart_json_rpc(params, request_id):
    if 'user_id' not in session:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {'code': 1, 'message': 'Not authorized'},
            'id': request_id
        })
    
    item_id = params.get('item_id')
    return remove_from_cart(item_id)

def create_order_json_rpc(params, request_id):
    if 'user_id' not in session:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {'code': 1, 'message': 'Not authorized'},
            'id': request_id
        })
    
    return create_order()

def get_cart_json_rpc(request_id):
    """JSON-RPC метод для получения корзины"""
    if 'user_id' not in session:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {'code': 1, 'message': 'Not authorized'},
            'id': request_id
        })
    
    conn, cur = db_connect()
    try:
        cur.execute('''
            SELECT c.*, p.name, p.price, p.image_url, p.stock 
            FROM cart c 
            JOIN product p ON c.product_id = p.id 
            WHERE c.user_id = ?
        ''', (session['user_id'],))
        cart_items = [dict(row) for row in cur.fetchall()]
        return jsonify({
            'jsonrpc': '2.0',
            'result': cart_items,
            'id': request_id
        })
    except Exception as e:
        return jsonify({
            'jsonrpc': '2.0',
            'error': {'code': -32000, 'message': str(e)},
            'id': request_id
        })
    finally:
        db_close(conn, cur)
