from flask import Flask, url_for, request, redirect
import datetime
app = Flask(__name__)




@app.route("/")
def index():
    return '''
<!doctype html> 
<html>
<head>
    <meta charset="utf-8">
    <title>Главная страница</title>
</head>
<body> 
    <h1>Главная страница</h1>
    <p>Добро пожаловать!</p>
</body> 
</html>
'''

@app.errorhandler(404)
def not_found(err):
    return "Нет такой страницы", 404

@app.route("/web")
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


@app.route("/author")
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

@app.route("/image")
def image():
    # Получаем пути правильно
    css_path = url_for("static", filename="lab1.css")
    image_path = url_for("static", filename="oak.jpg")
    
    return f'''
<!doctype html> 
<html>
    <head>
        <meta charset="utf-8">
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
@app.route("/counter")
def counter():
    global count
    count += 1
    time = datetime.datetime.today()
    url = request.url
    client_ip = request.remote_addr
    timestamp = datetime.datetime.now().timestamp()

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
        <a href="/reset?t={timestamp}">Сбросить счетчик</a>
    </body> 
</html>
'''

@app.route("/reset")
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
        <a href="/counter">Вернуться к счетчику</a>
    </body> 
</html>
'''

@app.route("/info")
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