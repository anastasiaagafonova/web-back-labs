




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