from flask import Flask, request, url_for
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from datetime import datetime
import os
from collections import Counter

app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "секретно-секретный секрет")
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'sqlite')
 
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)

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