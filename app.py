from flask import Flask, request, url_for
from flask_login import LoginManager
from db import db
from db.models import users, articles
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from rgz import rgz
from datetime import datetime
import os
from os import path
from collections import Counter
import secrets

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", secrets.token_hex(32))
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'sqlite')


login_manager = LoginManager()
login_manager.login_view = 'lab8.login'  
login_manager.login_message = "Пожалуйста, войдите для доступа к этой странице"
login_manager.login_message_category = "info"

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'anastasia_agafonova_orm'
    db_user = 'anastasia_agafonova_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "anastasia_agafonova_orm.db")  
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
login_manager.init_app(app)  

@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))

with app.app_context():
    db.create_all() 

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
app.register_blueprint(rgz)

LOG_FILE = os.path.join(os.path.dirname(__file__), '404_log.txt')  

@app.route("/")
@app.route("/index")
def index():
    return '''<!doctype html> 
<html>
<head>
    <title>НГТУ, ФБ, Лабораторные работы</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding-botton: 80px;
            line-height: 1.6;
        }
        header {
            background-color: gray;
            color: black;
            padding: 20px;
            text-align: left;
            left: 0;
        }
        nav {
            background-color: #f0f0f0;
            padding: 15px;
            margin: 20px 0;
        }
        nav ul {
            list-style-type: none;
            padding: 0;
        }
        nav li {
            margin: 10px 0;
        }
        nav a {
            text-decoration: none;
            color: #003366;
            font-weight: bold;
        }
        nav a:hover {
            color: #0066cc;
        }
        main {
            flex: 1;
            padding: 20px;
        }
        footer {
            background-color: gray;
            font-family: Arial, sans-serif;
            color: black;
            padding: 15px;
            text-align: right;
            position: fixed;
            bottom: 0;
            right: 0;
            z-index: 1000;
            width: 100%;
        }
    </style>
</head>
<body> 
    <header>
        <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
    </header>
    
    <body>
        <ul>
            <li><a href="/lab1">Лабораторная работа №1</a></li>
        </ul>
        <ul>
            <li><a href="/lab2">Лабораторная работа №2</a></li>
        </ul>
        <ul>
            <li><a href="/lab3">Лабораторная работа №3</a></li>
        </ul>
        <ul>
            <li><a href="/lab4">Лабораторная работа №4</a></li>
        </ul>
         <ul>
            <li><a href="/lab5">Лабораторная работа №5</a></li>
        </ul>
        <ul>
            <li><a href="/lab6">Лабораторная работа №6</a></li>
        </ul>
         <ul>
            <li><a href="/lab7">Лабораторная работа №7</a></li>
        </ul>
        <ul>
            <li><a href="/lab8">Лабораторная работа №8</a></li>
        </ul>
        <ul>
            <li><a href="/lab9">Лабораторная работа №9</a></li>
        </ul>
        <ul>
            <li><a href="/rgz">Магазин мебели "cozyhome"</a></li>
        </ul>
    </body>
    <footer>
        <p>Агафонова Анастасия, ФБИ-32, 3 курс, 2025</p>
    </footer>
</body> 
</html>
'''

@app.errorhandler(404)
def not_found(err):
    user_ip = request.remote_addr
    access_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    requested_url = request.url

    log_entry = f"{access_date} - IP: {user_ip} - URL: {requested_url}\n"
    try:
        with open(LOG_FILE, 'a', encoding='utf-8') as f:
            f.write(log_entry)
    except IOError as e:
        print(f"Log error: {e}")      
    try:
        with open(LOG_FILE, 'r', encoding='utf-8') as f:
            full_log = f.read()
    except FileNotFoundError:
        full_log = "No logs yet."
    except IOError:
        full_log = "Error reading log."
    root_link = '/'

    image_path = url_for("static", filename="404.jpg")  

    return f'''<!doctype html>
<html>
<head>
    <title>404</title>
    <style>
        body {{ font-family: monospace; margin: 20px; background: #f0f0f0; }}
        pre {{ background: white; padding: 10px; border: 1px solid #ccc; }}
        a {{ color: blue; text-decoration: none; }}
        img {{ max-width: 90%; max-height: 50vh; margin: 20px 0; border-radius: 8px; }}
    </style>
</head>
<body>
    <h1>404 - Not Found</h1>
    <p>IP: {user_ip}</p>
    <p>Date: {access_date}</p>
    <p>Requested: {requested_url}</p>
    <p><a href="{root_link}">На главную</a></p>

    <img src="{image_path}" alt="404 Error">
    
    <h3>Журнал:</h3>
    <pre>{full_log}</pre>
</body>
</html>'''


@app.errorhandler(500)
def internal_server_error(err):
    return '''<!doctype html> 
<html>
<head>
    <title>500 - Ошибка сервера</title>
</head>
<body> 
    <center>
        <h1 style="color:red;font-size:60px;">500</h1>
        <h2>Ошибка сервера</h2>
        <p>На сервере произошла ошибка</p>
        <p><a href="/test-errors">Назад</a></p>
    </center>
</body> 
</html>
''', 500


__all__ = ['app', 'db']