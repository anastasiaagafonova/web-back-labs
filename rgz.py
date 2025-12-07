from flask import Blueprint, url_for, request, render_template, make_response, redirect, session, current_app, jsonify
import re
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
from os import path

rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def lab():
    return render_template('lab5/lab5.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
                host='127.0.0.1',
                database='anastasia_agafonova_knowledge_base',
                user='anastasia_agafonova_knowledge_base',
                password='123'
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

@rgz.route('/rgz/')
def main():
    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM products2")
    else:
        cur.execute("SELECT * FROM products2")
    
    products = cur.fetchall()
    
    db_close(conn, cur)
    
    login = session.get('login')
    return render_template('rgz/rgz.html', products=products, login=login)

#валидация
def validate_latin_chars(text):
    if not text or not text.strip():
        return False, "Поле не может быть пустым"
    
    if not re.match(r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{};\':"\\|,.<>\/?]*$', text):
        return False, "Можно использовать только латинские буквы, цифры и знаки препинания"
    
    return True, ""
