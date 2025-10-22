from flask import Blueprint, redirect, url_for, render_template, request, make_response
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age')
    
    age_display = f"{age} лет" if age else None
    
    return render_template('lab3/lab3.html', 
                         name=name, 
                         name_color=name_color, 
                         age=age_display)


@lab3.route('/lab3/set_user_info', methods=['POST'])
def set_user_info():
    name = request.form.get('name')
    name_color = request.form.get('name_color')
    age = request.form.get('age')
    
    resp = make_response(redirect('/lab3/'))
    
    if name:
        resp.set_cookie('name', name)
    if name_color:
        resp.set_cookie('name_color', name_color)
    if age:
        resp.set_cookie('age', age)
    
    return resp

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age', '20')
    resp.set_cookie('name_color', 'magenta')
    return resp

@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    
    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)
    

@lab3.route('/lab3/success')
def success():
    price = request.args.get('price', 0)
    return render_template('lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_family = request.args.get('font_family')
    margin = request.args.get('margin')
    
    if any([color, bg_color, font_size, font_family, margin]):
        resp = make_response(redirect('/lab3/settings'))
        if color:
            resp.set_cookie('color', color)
        if bg_color:
            resp.set_cookie('bg_color', bg_color)
        if font_size:
            resp.set_cookie('font_size', font_size)
        if font_family:
            resp.set_cookie('font_family', font_family)
        if margin:
            resp.set_cookie('margin', margin)
        return resp
    
    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size')
    font_family = request.cookies.get('font_family')
    margin = request.cookies.get('margin')
    
    resp = make_response(render_template('lab3/settings.html', 
                                       color=color, 
                                       bg_color=bg_color, 
                                       font_size=font_size, 
                                       font_family=font_family,
                                       margin=margin))
    return resp


@lab3.route('/lab3/ticket')
def ticket_form():
    return render_template('lab3/ticketform.html', errors={})

@lab3.route('/lab3/ticketresult', methods=['POST'])
def ticket_result():
    fio = request.form.get('fio')
    shelf = request.form.get('shelf')
    bedding = request.form.get('bedding')
    luggage = request.form.get('luggage')
    age = request.form.get('age')
    departure = request.form.get('departure')
    destination = request.form.get('destination')
    date = request.form.get('date')
    insurance = request.form.get('insurance')
    
    errors = {}
    
    if not fio:
        errors['fio'] = 'Введите ФИО пассажира'
    if not shelf:
        errors['shelf'] = 'Выберите тип полки'
    if not bedding:
        errors['bedding'] = 'Укажите наличие белья'
    if not luggage:
        errors['luggage'] = 'Укажите наличие багажа'
    if not age:
        errors['age'] = 'Введите возраст'
    elif not age.isdigit() or not (1 <= int(age) <= 120):
        errors['age'] = 'Возраст должен быть от 1 до 120 лет'
    if not departure:
        errors['departure'] = 'Введите пункт выезда'
    if not destination:
        errors['destination'] = 'Введите пункт назначения'
    if not date:
        errors['date'] = 'Выберите дату поездки'
    if not insurance:
        errors['insurance'] = 'Укажите наличие страховки'
    
    # Если есть ошибки - показываем форму снова
    if errors:
        return render_template('lab3/ticketform.html', 
                             errors=errors,
                             fio=fio or '', 
                             shelf=shelf or '',
                             bedding=bedding or '', 
                             luggage=luggage or '', 
                             age=age or '', 
                             departure=departure or '',
                             destination=destination or '', 
                             date=date or '', 
                             insurance=insurance or '')
    
    age_int = int(age)
    if age_int < 18:
        ticket_type = "Детский билет"
        base_price = 700
    else:
        ticket_type = "Взрослый билет"
        base_price = 1000
    
    total_price = base_price
    
    if shelf in ['нижняя', 'нижняя боковая']:
        total_price += 100  # доплата за нижнюю полку
    
    if bedding == 'да':
        total_price += 75   # доплата за бельё
    
    if luggage == 'да':
        total_price += 250  # доплата за багаж
    
    if insurance == 'да':
        total_price += 150  # доплата за страховку
    
    return render_template('lab3/ticketresult.html',
                         fio=fio, 
                         shelf=shelf, 
                         bedding=bedding,
                         luggage=luggage, 
                         age=age, 
                         departure=departure,
                         destination=destination, 
                         date=date, 
                         insurance=insurance,
                         ticket_type=ticket_type, 
                         total_price=total_price)
                         
@lab3.route('/lab3/clearsettings')
def clear_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.delete_cookie('color')
    resp.delete_cookie('bg_color') 
    resp.delete_cookie('font_size')
    resp.delete_cookie('font_family')
    return resp


products = [
    {"name": "iPhone 15", "price": 89990, "brand": "Apple", "color": "черный", "storage": "128GB", "image": "1.jpg"},
    {"name": "Samsung Galaxy S24", "price": 79990, "brand": "Samsung", "color": "белый", "storage": "256GB", "image": "2.jpg"},
    {"name": "Xiaomi 14", "price": 59990, "brand": "Xiaomi", "color": "синий", "storage": "256GB", "image": "3.jpg"},
    {"name": "Google Pixel 8", "price": 69990, "brand": "Google", "color": "серый", "storage": "128GB", "image": "4.jpg"},
    {"name": "OnePlus 12", "price": 64990, "brand": "OnePlus", "color": "зеленый", "storage": "256GB", "image": "5.jpg"},
    {"name": "iPhone 14", "price": 69990, "brand": "Apple", "color": "красный", "storage": "128GB", "image": "6.jpg"},
    {"name": "Samsung Galaxy A54", "price": 34990, "brand": "Samsung", "color": "фиолетовый", "storage": "128GB", "image": "7.jpg"},
    {"name": "Xiaomi Redmi Note 13", "price": 24990, "brand": "Xiaomi", "color": "черный", "storage": "128GB", "image": "8.jpg"},
    {"name": "Realme 11 Pro", "price": 29990, "brand": "Realme", "color": "золотой", "storage": "256GB", "image": "9.jpg"},
    {"name": "Nothing Phone 2", "price": 45990, "brand": "Nothing", "color": "белый", "storage": "256GB", "image": "10.jpg"},
    {"name": "iPhone 13", "price": 59990, "brand": "Apple", "color": "розовый", "storage": "128GB", "image": "11.jpg"},
    {"name": "Samsung Galaxy Z Flip5", "price": 99990, "brand": "Samsung", "color": "фиолетовый", "storage": "256GB", "image": "12.jpg"},
    {"name": "Xiaomi Poco X6", "price": 27990, "brand": "Xiaomi", "color": "желтый", "storage": "128GB", "image": "13.jpg"},
    {"name": "Google Pixel 7a", "price": 44990, "brand": "Google", "color": "синий", "storage": "128GB", "image": "14.jpg"},
    {"name": "OnePlus Nord 3", "price": 37990, "brand": "OnePlus", "color": "серый", "storage": "256GB", "image": "15.jpg"},
    {"name": "iPhone SE", "price": 15990, "brand": "Apple", "color": "белый", "storage": "64GB", "image": "16.jpg"},
    {"name": "Samsung Galaxy M54", "price": 29990, "brand": "Samsung", "color": "синий", "storage": "128GB", "image": "17.jpg"},
    {"name": "Xiaomi 13T", "price": 49990, "brand": "Xiaomi", "color": "черный", "storage": "256GB", "image": "18.jfif"},
    {"name": "Realme GT 2", "price": 39990, "brand": "Realme", "color": "стальной", "storage": "128GB", "image": "19.jpg"},
    {"name": "iPhone 15 pro", "price": 89990, "brand": "Apple", "color": "натуральный титан", "storage": "256GB", "image": "20.jpg"}
]

@lab3.route('/lab3/products')
def products_search():
    min_price_form = request.args.get('min_price')
    max_price_form = request.args.get('max_price')
    
    min_price_cookie = request.cookies.get('min_price')
    max_price_cookie = request.cookies.get('max_price')
    
    min_price = min_price_form if min_price_form is not None else (min_price_cookie or '')
    max_price = max_price_form if max_price_form is not None else (max_price_cookie or '')
    
    filtered_products = products.copy()
    
    if min_price or max_price:
        try:
            min_val = float(min_price) if min_price else 0
            max_val = float(max_price) if max_price else float('inf')
            
            if min_val > max_val:
                min_val, max_val = max_val, min_val
                min_price, max_price = max_price, min_price
            
            filtered_products = [
                p for p in products 
                if (not min_price or p['price'] >= min_val) and 
                   (not max_price or p['price'] <= max_val)
            ]
            
            # Сохраняем в куки
            resp = make_response(render_template('lab3/products.html', 
                                               products=products,
                                               min_price=min_price,
                                               max_price=max_price,
                                               filtered_products=filtered_products,
                                               count=len(filtered_products)))
            if min_price:
                resp.set_cookie('min_price', min_price)
            if max_price:
                resp.set_cookie('max_price', max_price)
            return resp
            
        except ValueError:
            pass
    
    return render_template('lab3/products.html', 
                         products=products,
                         min_price=min_price,
                         max_price=max_price,
                         filtered_products=filtered_products,
                         count=len(filtered_products))

@lab3.route('/lab3/products_reset')
def products_reset():
    resp = make_response(redirect('/lab3/products'))
    resp.delete_cookie('min_price')
    resp.delete_cookie('max_price')
    return resp