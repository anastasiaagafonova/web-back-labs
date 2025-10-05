from flask import Flask, url_for, request, redirect, abort, render_template
from datetime import datetime
import os
from collections import Counter
app = Flask(__name__)

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

@app.route("/lab1")
def lab1_index():
    return '''<!doctype html> 
<html>
<head>
    <title>Лабораторная 1</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            min-height: 100vh;
            padding: 0;
            margin: 0;
            display: flex;
            flex-direction: column;
        }
        header {
            background-color: gray;
            color: black;
            padding: 20px;
            text-align: left;
            width: 100%;
        }
        main {
            flex: 1;
            padding: 20px;
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
        }
        .description {
            background-color: #f9f9f9;
            padding: 20px;
            border-left: 4px solid #003366;
            margin: 20px 0;
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
        <h1>Лабораторная работа 1</h1>
    </header>

    <main>
        <div class="description">
            <p><strong>Flask</strong> — фреймворк для создания веб-приложений на языке программирования Python, 
            использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. Относится к категории так 
            называемых микрофреймворков — минималистичных каркасов веб-приложений, сознательно предоставляющих 
            лишь самые базовые возможности.</p>
        </div>

        <h2>Разделы лабораторной работы:</h2>
        <ul>
            <li><a href="/lab1/web">Web</a></li>
            <li><a href="/lab1/author">Author</a></li>
            <li><a href="/lab1/image">Image</a></li>
            <li><a href="/lab1/counter">Counter</a></li>
            <li><a href="/lab1/created">Created</a></li>
            <li><a href="/lab1/info">Info</a></li>
            <li><a href="/errors">Errors</a></li>
            <li><a href="/test-errors">505</a></li>
            <li><a href="/404">404</a></li>
        </ul>
        
        <br>
        <a href="/">Вернуться на главную страницу</a>
    </main>

    <footer>
        <p>Агафонова Анастасия, ФБИ-32, 3 курс, 2025</p>
    </footer>
</body> 
</html>
'''

@app.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html>
           <body> 
               <h1>web-сервер на flask</h1> 
               <a href="/author">author</a>
           </body> 
        </html>""", 200, {
            'X-Server': 'sample',
            'Content-Type': 'text/plain; charset=utf-8',
            'Author': 'agafonova'
        }


@app.route("/lab1/author")
def author():
    name = "Агафонова Анастасия Степановна"
    group = "ФБИ-32"
    faculty = "ФБ"

    return """<!doctype html> 
        <html>
           <body> 
               <p>Студент: """ + name + """</p> 
               <p>Группа: """ + group + """</p> 
               <p>Факультет: """ + faculty + """</p> 
               <a href="/web">web</a>
           </body> 
        </html>"""

@app.route("/lab1/image")
def image():
    css_path = url_for("static", filename="lab1.css")
    image_path = url_for("static", filename="oak.jpg")
    headers = {
        'Content-Language': 'en-EN',
        'X-Custom-Header-1': 'Oak',
        'X-Custom-Header-2': 'Flask'
    }
    return f'''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body>
        <div class="container">
            <h1>Дуб</h1>
            <img src="{image_path}">
        </div>
    </body>
</html>
''', 200, headers

count = 0
@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return ''' <!doctype html> 
<html>
<head>
    <title>Счетчик</title>
</head>
<body> 
    <h2>Счетчик посещений</h2>
    <p>Сколько раз вы сюда заходили: <strong>''' + str(count) + '''</strong></p>
    <hr>
    <p>Дата и время: ''' + str(time) + '''</p>
    <p>Запрошенный адрес: ''' + str(url) + '''</p>
    <p>Ваш IP-адрес: ''' + str(client_ip) + '''</p>
    <br>
    <a href="/lab1/reset">Сбросить счетчик</a>
</body> 
</html>
'''

@app.route("/lab1/reset")
def reset_counter():
    global count
    count = 0
    return ''' <!doctype html> 
<html>
<head>
    <meta charset="utf-8">
    <title>Сброс счетчика</title>
</head>
<body> 
    <h2>Счетчик сброшен!</h2>
    <p>Текущее значение счетчика: <strong>''' + str(count) + '''</strong></p>
    <a href="/lab1/counter">Вернуться к счетчику</a>
</body> 
</html>
'''

@app.route("/lab1/info")
def info():
    return redirect ("/lab1/author")

@app.route("/lab1/created")
def created():
    return ''' <!doctype html> 
        <html>
            <body> 
                <h1>Создано успешно</h1> 
                <div><i>что-то создано...</i></div>
            </body> 
        </html>
        ''',201

@app.route("/400")
def bad_request():
    return ''' <!doctype html> 
<head>
    <title>400 Bad Request</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .error { color: #d63384; background-color: #f8f9fa; padding: 20px; border-left: 4px solid #d63384; }
    </style>
</head>
<body> 
    <h1>400 Bad Request</h1>
    <div class="error">
        <p><strong>Ошибка 400:</strong> Сервер не может обработать запрос из-за синтаксической ошибки клиента.</p>
        <p>Возможные причины: неверный синтаксис запроса, неверный размер запроса, неверный заголовок и т.д.</p>
    </div>
    <a href="/errors">Назад</a>
</body> 
</html>
''', 400

@app.route("/401")
def unauthorized():
    return ''' <!doctype html> 
<head>
    <title>401 Unauthorized</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .error { color: #fd7e14; background-color: #fff3cd; padding: 20px; border-left: 4px solid #fd7e14; }
    </style>
</head>
<body> 
    <h1>401 Unauthorized</h1>
    <div class="error">
        <p><strong>Ошибка 401:</strong> Требуется аутентификация для доступа к ресурсу.</p>
        <p>Запрос не был применён, так как он не содержит корректные учётные данные для целевого ресурса.</p>
    </div>
    <a href="/errors">Назад</a>
</body> 
</html>
''', 401

@app.route("/402")
def payment_required():
    return ''' <!doctype html> 
<html>
<head>
    <title>402 Payment Required</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .error { color: #20c997; background-color: #d1f2eb; padding: 20px; border-left: 4px solid #20c997; }
    </style>
</head>
<body> 
    <h1>402 Payment Required</h1>
    <div class="error">
        <p><strong>Ошибка 402:</strong> Требуется оплата для доступа к ресурсу.</p>
        <p>Этот код зарезервирован для будущего использования. Изначально предназначался для цифровых платежных систем.</p>
    </div>
    <a href="/errors">Назад</a>
</body> 
</html>
''', 402

@app.route("/403")
def forbidden():
    return ''' <!doctype html> 
<html>
<head>
    <title>403 Forbidden</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .error { color: #dc3545; background-color: #f8d7da; padding: 20px; border-left: 4px solid #dc3545; }
    </style>
</head>
<body> 
    <h1>403 Forbidden</h1>
    <div class="error">
        <p><strong>Ошибка 403:</strong> Доступ к запрошенному ресурсу запрещён.</p>
        <p>Сервер понял запрос, но отказывается его авторизовать. В отличие от 401, аутентификация не поможет.</p>
    </div>
    <a href="/errors">Назад</a>
</body> 
</html>
''', 403

@app.route("/405")
def method_not_allowed():
    return ''' <!doctype html> 
<html>
<head>
    <title>405 Method Not Allowed</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .error { color: #6f42c1; background-color: #e9ecef; padding: 20px; border-left: 4px solid #6f42c1; }
    </style>
</head>
<body> 
    <h1>405 Method Not Allowed</h1>
    <div class="error">
        <p><strong>Ошибка 405:</strong> Метод запроса не поддерживается для данного ресурса.</p>
        <p>Например, попытка использовать POST для ресурса, который поддерживает только GET.</p>
    </div>
    <a href="/errors">Назад</a>
</body> 
</html>
''', 405

@app.route("/418")
def teapot():
    return ''' <!doctype html> 
<html>
<head>
    <title>418 I'm a teapot</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; }
        .error { color: #6f42c1; background-color: #e9ecef; padding: 20px; border-left: 4px solid #6f42c1; }
    </style>
</head>
<body> 
    <h1>418 I'm a teapot</h1>
    <div class="error">
        <p><strong>Ошибка 418:</strong> Я - чайник!</p>
        <p>Это шуточный код ошибки из RFC 2324 (Hyper Text Coffee Pot Control Protocol).</p>
        <p>Сервер отказывается заваривать кофе, потому что он является чайником.</p>
    </div>
    <a href="/errors">Назад</a>
</body> 
</html>
''', 418


@app.route("/errors")
def errors_list():
    return ''' <!doctype html> 
<head>
    <title>HTTP Error Codes</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }
        .error-list { list-style-type: none; padding: 0; }
        .error-list li { margin: 10px 0; padding: 10px; background-color: #f8f9fa; border-left: 4px solid #007bff; }
        .error-list a { text-decoration: none; color: #007bff; font-weight: bold; }
        .error-list a:hover { color: #0056b3; }
    </style>
</head>
<body> 
    <h1>HTTP Коды ошибок для тестирования</h1>
    <p>Выберите код ошибки для просмотра:</p>
    
    <ul class="error-list">
        <li><a href="/400">400 Bad Request</a> - Неверный запрос</li>
        <li><a href="/401">401 Unauthorized</a> - Неавторизованный доступ</li>
        <li><a href="/402">402 Payment Required</a> - Требуется оплата</li>
        <li><a href="/403">403 Forbidden</a> - Доступ запрещён</li>
        <li><a href="/405">405 Method Not Allowed</a> - Метод не разрешён</li>
        <li><a href="/418">418 I'm a teapot</a> - Я - чайник! (шуточный код)</li>
    </ul>
    
    <a href="/">На главную</a>
</body> 
</html>
'''

@app.route("/cause-error")
def cause_error():
    error_type = request.args.get('type', 'division')
    
    if error_type == 'division':
        # Деление на ноль
        result = 10 / 0
    elif error_type == 'concatenation':
        # Конкатенация числа и строки
        result = 10 + "строка"
    elif error_type == 'undefined':
        # Обращение к неопределенной переменной
        result = undefined_variable
    

@app.route("/test-errors")
def test_errors():
    return ''' <!doctype html> 
<html>
<head>
    <title>Тестирование ошибок сервера</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; max-width: 800px; margin: 0 auto; }
        .error-type { 
            display: block; 
            margin: 10px 0; 
            padding: 15px; 
            background-color: #f8f9fa; 
            border-left: 4px solid #dc3545;
            text-decoration: none;
            color: #333;
            transition: background-color 0.3s;
        }
        .error-type:hover { 
            background-color: #e9ecef; 
            text-decoration: none;
        }
        .warning { 
            background-color: #fff3cd; 
            border-left: 4px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
        }
    </style>
</head>
<body> 
    <h1>Тестирование ошибок сервера (500)</h1>
    
    <a href="/cause-error?type=division" class="error-type">
        <strong>Деление на ноль</strong><br>
        <small>result = 10 / 0</small>
    </a>
    
    <a href="/cause-error?type=concatenation" class="error-type">
        <strong>Конкатенация числа и строки</strong><br>
        <small>result = 10 + "строка"</small>
    </a>
    
    <a href="/cause-error?type=undefined" class="error-type">
        <strong>Неопределенная переменная</strong><br>
        <small>result = undefined_variable</small>
    </a>
    <br>
    <a href="/">На главную</a>
</body> 
</html>
'''

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

flower_list = [
    {'name': 'роза', 'price': 10},
    {'name': 'тюльпан', 'price': 5},
    {'name': 'незабудка', 'price': 2},
    {'name': 'ромашка', 'price': 3}
]

@app.route('/lab2/a/')
def a():
    return 'ok'

@app.route('/lab2/flowers/<int:flower_id>')
def flowers(flower_id):
    if flower_id >= len(flower_list) or flower_id < 0:
        abort(404)
    flower = flower_list[flower_id]
    return render_template('flower.html', flower=flower, flower_id=flower_id)

@app.route('/lab2/add/flower/', methods=['POST'])
def add_flower():
    name = request.form.get('name', '').strip()
    price_str = request.form.get('price', '').strip()
    if not name or not price_str:
        return "Заполните все поля!", 400
    try:
        price = float(price_str)
        if price < 0:
            return "Цена не может быть отрицательной!", 400
    except ValueError:
        return "Цена должна быть числом!", 400
    flower_list.append({'name': name, 'price': price})
    return redirect(url_for('all_flowers_html'))

@app.route('/lab2/flowers_html')
def all_flowers_html():
    return render_template('all_flowers.html', flowers=flower_list, count=len(flower_list))

@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('all_flowers_html'))

@app.route('/lab2/flowers/<int:flower_id>/delete')
def delete_flower(flower_id):
    if flower_id >= len(flower_list) or flower_id < 0:
        abort(404)
    del flower_list[flower_id]
    return redirect(url_for('all_flowers_html'))


@app.route('/lab2/example')
def example():
    name = 'Анастасия Агафонова'
    group = 'ФБИ-32'
    number = '2'
    cours = '3'
    fruits = [
        {'name': 'яблоки', 'price': 100},
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 195},
        {'name': 'манго', 'price': 321}
    ]
    return render_template('example.html', name=name, group=group, number=number, cours=cours, fruits=fruits  )
    
@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase = phrase)

@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    try:
        divide_result = a / b
    except ZeroDivisionError:
        divide_result = 'Ошибка: деление на ноль'
    
    operations = {
        'sum': a + b,
        'subtract': a - b,
        'multiply': a * b,
        'divide': divide_result,
        'power': a ** b
    }
    return render_template('calc.html', a=a, b=b, operations=operations)

@app.route('/lab2/calc/')
def calc_default():
    return redirect('/lab2/calc/1/1')

@app.route('/lab2/calc/<int:a>')
def calc_single(a):
    return redirect(f'/lab2/calc/{a}/1')

books_list= [
    {'author': 'Фрэнк Герберт', 'title': 'Дюна', 'genre': 'Научная фантастика', 'pages': 736},
    {'author': 'Джордж Оруэлл', 'title': '1984', 'genre': 'Антиутопия', 'pages': 328},
    {'author': 'Рэй Брэдбери', 'title': '451° по Фаренгейту', 'genre': 'Антиутопия', 'pages': 256},
    {'author': 'Харуки Мураками', 'title': 'Норвежский лес', 'genre': 'Роман', 'pages': 400},
    {'author': 'Стивен Кинг', 'title': 'Оно', 'genre': 'Ужасы', 'pages': 1248},
    {'author': 'Джон Р. Р. Толкин', 'title': 'Властелин Колец', 'genre': 'Фэнтези', 'pages': 1120},
    {'author': 'Агата Кристи', 'title': 'Убийство в Восточном экспрессе', 'genre': 'Детектив', 'pages': 320},
    {'author': 'Артур Конан Дойл', 'title': 'Шерлок Холмс: Сборник рассказов', 'genre': 'Детектив', 'pages': 380},
    {'author': 'Энди Вейер', 'title': 'Марсианин', 'genre': 'Научная фантастика', 'pages': 384},
    {'author': 'Пауло Коэльо', 'title': 'Алхимик', 'genre': 'Философская притча', 'pages': 208},
    {'author': 'Дуглас Адамс', 'title': 'Автостопом по галактике', 'genre': 'Юмористическая фантастика', 'pages': 320},
    {'author': 'Джек Лондон', 'title': 'Белый Клык', 'genre': 'Приключения', 'pages': 272}
]

@app.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books_list)

cars_list = [
    {
        'name': 'Lamborghini Huracan',
        'image': 'Lamborghini huracan.jpg',
        'description': 'Итальянский суперкар с двигателем V10, 640 л.с., разгон до 100 км/ч за 2.9 секунды.'
    },
    {
        'name': 'Ford Mustang',
        'image': 'Ford Mustang.jpg',
        'description': 'Легендарный американский маслкар с двигателем V8, 450 л.с., задним приводом.'
    },
    {
        'name': 'BMW M5',
        'image': 'bmw m5.jpg',
        'description': 'Немецкий спортивный седан с двигателем V8 4.4 л, 600 л.с., полным приводом xDrive.'
    },
    {
        'name': 'Audi RS6',
        'image': 'Audi RS6.jpg',
        'description': 'Универсал с характером суперкара, 4.0 л V8, 600 л.с., полный привод quattro.'
    },
    {
        'name': 'Ferrari F8 Tributo',
        'image': 'Ferrari F8 Tributo.jpg',
        'description': 'Среднемоторный итальянский суперкар с двигателем V8, 720 л.с., 2.9 сек до 100 км/ч.'
    },
    {
        'name': 'Lexus LX 570',
        'image': 'Лексус 570.jpg',
        'description': 'Роскошный полноразмерный внедорожник с двигателем V8 5.7 л и высочайшим комфортом.'
    },
    {
        'name': 'Subaru WRX STI',
        'image': 'Subaru WRX STI.jpg',
        'description': 'Японский полноприводный седан с оппозитным двигателем 2.5 л, 310 л.с., для ралли.'
    },
    {
        'name': 'Nissan GT-R',
        'image': 'Nissan GT-R.jpg',
        'description': 'Японский суперкар "Бог" с двигателем V6 3.8 л, 570 л.с., полным приводом.'
    },
    {
        'name': 'Chevrolet Corvette',
        'image': 'Chevrolet Corvette.jpg',
        'description': 'Американский спорткар с двигателем V8, 495 л.с., задним приводом.'
    },
    {
        'name': 'Lexus IS',
        'image': 'Лексус.jpg',
        'description': 'Компактный премиальный седан с элегантным дизайном и отличной надежностью.'
    },
    {
        'name': 'Range Rover Sport',
        'image': 'Range Rover Sport.jpg',
        'description': 'Британский премиальный внедорожник с роскошным салоном и отличной проходимостью.'
    },
    {
        'name': 'Dodge Challenger SRT Hellcat',
        'image': 'машина.jpg',
        'description': 'Американский маслкар с двигателем V8 6.2 л, 717 л.с., задним приводом.'
    },
    {
        'name': 'Honda Civic Type R',
        'image': 'Honda Civic Type R.jpg',
        'description': 'Горячий хетчбек с турбодвигателем 2.0 л, 320 л.с., передним приводом.'
    },
    {
        'name': 'Jeep Wrangler',
        'image': 'Jeep Wrangler.jpg',
        'description': 'Легендарный внедорожник с рамной конструкцией, съемными дверями и складной крышей.'
    },
    {
        'name': 'Volvo XC90',
        'image': 'Volvo XC90.jpg',
        'description': 'Шведский премиальный внедорожник с скандинавским дизайном и системами безопасности.'
    },
    {
        'name': 'Hyundai Tucson',
        'image': 'Hyundai Tucson.jpg',
        'description': 'Современный кроссовер с агрессивным дизайном, богатым оснащением и надежностью.'
    },
    {
        'name': 'Kia K5',
        'image': 'Kia K5.jpg',
        'description': 'Спортивный седан с ярким дизайном, турбодвигателями и отличной комплектацией.'
    },
    {
        'name': 'McLaren 720S',
        'image': 'McLaren 720S.jpg',
        'description': 'Британский суперкар с карбоновым монококом, 720 л.с., 2.9 сек до 100 км/ч.'
    }
]

@app.route('/lab2/cars')
def show_cars():
    return render_template('cars.html', cars=cars_list)

@app.route('/lab2/test-images')
def test_images():
    return '''
    <h1>Тест статических файлов</h1>
    <img src="{{ url_for('static', filename='images/cars/lamborghini_huracan.jpg') }}" width="200">
    <p>Если картинка не отображается, проверьте путь и файл</p>
    '''