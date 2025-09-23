from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)




# Главная страница на корневом адресе
@app.route("/")
def index():
    return '''
<!doctype html> 
<html lang="ru">
<head>
    <meta charset="utf-8">
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
            <li><a href="/lab1">Первая лабораторная работа</a></li>
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
    return "Нет такой страницы", 404

@app.route("/lab1")
def lab1_index():
    return '''
<!doctype html> 
<html lang="ru">
<head>
    <meta charset="utf-8">
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
            'Content-Type': 'text/plain; charset=utf-8'
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
    # Получаем пути правильно
    css_path = url_for("static", filename="lab1.css")
    image_path = url_for("static", filename="oak.jpg")
    
    return f'''
<!doctype html> 
<html>
    <head>
        <title>Дуб</title>
        <link rel="stylesheet" href="{css_path}">
    </head>
    <body> 
        <h1>Дуб</h1> 
        <img src="{image_path}" alt="Дуб">
    </body> 
</html>
'''

count = 0
@app.route("/lab1/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr

    return '''
<!doctype html> 
<html>
    <head>
        <meta charset="utf-8">
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
    return '''
<!doctype html> 
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
    return redirect ("/author")

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
    return '''
<!doctype html> 
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
    return '''
<!doctype html> 
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
    return '''
<!doctype html> 
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
    return '''
<!doctype html> 
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
    return '''
<!doctype html> 
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
    return '''
<!doctype html> 
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
    return '''
<!doctype html> 
<html lang="ru">
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
    
    <p>Для просмотра кода ответа откройте инструменты разработчика (F12) → вкладка "Network"</p>
    
    <a href="/">На главную</a>
</body> 
</html>
'''

if __name__ == "__main__":
    app.run(debug=True)