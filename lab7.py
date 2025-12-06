from flask import Blueprint, url_for, request, render_template, make_response, redirect, session, current_app, abort, jsonify
from datetime import datetime
import sqlite3
from pathlib import Path

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

def get_db_connection():
    """Создает соединение с базой данных SQLite"""
    current_dir = Path(__file__).parent
    db_path = current_dir / "database.db"
    
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def film_to_dict(row):
    """Преобразует запись из БД в словарь"""
    return {
        'id': row['id'],
        'title': row['title'],
        'title_ru': row['title_ru'],
        'year': row['year'],
        'description': row['description']
    }

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    """Получить все фильмы из БД"""
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM films ORDER BY id")
        films = cursor.fetchall()
        
        films_list = [film_to_dict(film) for film in films]
        return jsonify(films_list)
    finally:
        conn.close()

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    """Получить один фильм по ID"""
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM films WHERE id = ?", (id,))
        film = cursor.fetchone()
        
        if film is None:
            abort(404, description=f"Film with id {id} not found")
        
        return jsonify(film_to_dict(film))
    finally:
        conn.close()

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    """Удалить фильм по ID"""
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM films WHERE id = ?", (id,))
        film = cursor.fetchone()
        
        if film is None:
            abort(404, description=f"Film with id {id} not found")
        
        film_name = film['title_ru']
        
        cursor.execute("DELETE FROM films WHERE id = ?", (id,))
        conn.commit()
        
        return jsonify({
            "message": f"Фильм '{film_name}' удален",
            "id": id
        }), 200
    finally:
        conn.close()

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    """Обновить фильм по ID"""
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM films WHERE id = ?", (id,))
        film = cursor.fetchone()
        
        if film is None:
            abort(404, description=f"Film with id {id} not found")
        
        data = request.get_json()
        
        # Проверка русского названия
        if 'title_ru' not in data or not data['title_ru'].strip():
            return jsonify({'title_ru': 'Русское название обязательно'}), 400
        
        # Проверка оригинального названия (если русское пустое)
        if not data.get('title') and not data.get('title_ru'):
            return jsonify({'title': 'Оригинальное название обязательно, если русское пустое'}), 400
        
        # Проверка года
        if 'year' not in data:
            return jsonify({'year': 'Год обязателен'}), 400
        
        try:
            year = int(data['year'])
        except ValueError:
            return jsonify({'year': 'Год должен быть числом'}), 400
        
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            return jsonify({'year': f'Год должен быть от 1895 до {current_year}'}), 400
        
        # Проверка описания
        if 'description' not in data:
            return jsonify({'description': 'Описание обязательно'}), 400
        
        description = data['description']
        if not description.strip():
            return jsonify({'description': 'Заполните описание'}), 400
        
        if len(description) > 2000:
            return jsonify({'description': 'Описание не должно превышать 2000 символов'}), 400
        
        # Если оригинальное название не указано, используем русское
        title = data.get('title')
        if not title:
            title = data['title_ru']
        
        # Обновляем запись
        cursor.execute('''
            UPDATE films 
            SET title = ?, title_ru = ?, year = ?, description = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, data['title_ru'], year, description, id))
        
        conn.commit()
        
        cursor.execute("SELECT * FROM films WHERE id = ?", (id,))
        updated_film = cursor.fetchone()
        
        return jsonify(film_to_dict(updated_film))
    finally:
        conn.close()

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    """Добавить новый фильм"""
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()
        data = request.get_json()
        
        # Проверка русского названия
        if 'title_ru' not in data or not data['title_ru'].strip():
            return jsonify({'title_ru': 'Русское название обязательно'}), 400
        
        # Проверка оригинального названия (если русское пустое)
        if not data.get('title') and not data.get('title_ru'):
            return jsonify({'title': 'Оригинальное название обязательно, если русское пустое'}), 400
        
        # Проверка года
        if 'year' not in data:
            return jsonify({'year': 'Год обязателен'}), 400
        
        try:
            year = int(data['year'])
        except ValueError:
            return jsonify({'year': 'Год должен быть числом'}), 400
        
        current_year = datetime.now().year
        if year < 1895 or year > current_year:
            return jsonify({'year': f'Год должен быть от 1895 до {current_year}'}), 400
        
        # Проверка описания
        if 'description' not in data:
            return jsonify({'description': 'Описание обязательно'}), 400
        
        description = data['description']
        if not description.strip():
            return jsonify({'description': 'Заполните описание'}), 400
        
        if len(description) > 2000:
            return jsonify({'description': 'Описание не должно превышать 2000 символов'}), 400
        
        # Если оригинальное название не указано, используем русское
        title = data.get('title')
        if not title:
            title = data['title_ru']
        
        # Добавляем новый фильм
        cursor.execute('''
            INSERT INTO films (title, title_ru, year, description)
            VALUES (?, ?, ?, ?)
        ''', (title, data['title_ru'], year, description))
        
        conn.commit()
        
        new_id = cursor.lastrowid
        cursor.execute("SELECT * FROM films WHERE id = ?", (new_id,))
        new_film = cursor.fetchone()
        
        return jsonify(film_to_dict(new_film)), 201
    finally:
        conn.close()