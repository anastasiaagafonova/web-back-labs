from flask import Blueprint, redirect, render_template, request, session

lab4 = Blueprint('lab4', __name__)

tree_count = 0
max_trees = 5

users = [
    {'login': 'alex', 'password': '123', 'name': 'Александр', 'gender': 'мужской'},
    {'login': 'bob', 'password': '555', 'name': 'Роберт', 'gender': 'мужской'},
    {'login': 'anna', 'password': '777', 'name': 'Анна', 'gender': 'женский'},
    {'login': 'mary', 'password': '888', 'name': 'Мария', 'gender': 'женский'},
]


@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')

@lab4.route('/lab4/div', methods=['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if not x1 or not x2:
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены')
    
    try:
        x1 = int(x1)
        x2 = int(x2)
    except ValueError:
        return render_template('lab4/div.html', error='Поля должны содержать числа')
    
    if x2 == 0:
        return render_template('lab4/div.html', error='Деление на ноль невозможно')
    
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 else 0
    x2 = int(x2) if x2 else 0
    
    result = x1 + x2
    return render_template('lab4/sum.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    x1 = int(x1) if x1 else 1
    x2 = int(x2) if x2 else 1
    
    result = x1 * x2
    return render_template('lab4/mul.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if not x1 or not x2:
        return render_template('lab4/sub.html', error='Оба поля должны быть заполнены')
    
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    
    return render_template('lab4/sub.html', x1=x1, x2=x2, result=result)

@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if not x1 or not x2:
        return render_template('lab4/pow.html', error='Оба поля должны быть заполнены')
    
    x1 = int(x1)
    x2 = int(x2)

    if x1 == 0 and x2 == 0:
        return render_template('lab4/pow.html', error='Оба числа не могут быть равны нулю')
    
    result = x1 ** x2
    return render_template('lab4/pow.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count, max_trees=max_trees)

    operation = request.form.get('operation')

    if operation == 'cut' and tree_count > 0:
        tree_count -= 1
    elif operation == 'plant' and tree_count < max_trees:
        tree_count += 1

    return redirect('/lab4/tree')


@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'login' in session:
            authorized = True
            login = session['login']
            user_name = next((user['name'] for user in users if user['login'] == login), login)
        else:
            authorized = False
            login = ''
            user_name = ''
        
        return render_template('lab4/login.html', authorized=authorized, login=login, user_name=user_name)
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not login:
        return render_template('lab4/login.html', error='Не введён логин', authorized=False, login=login)
    
    if not password:
        return render_template('lab4/login.html', error='Не введён пароль', authorized=False, login=login)
    
    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['user_name'] = user['name']
            return redirect('/lab4/login')
    
    error = 'Неверные логин и/или пароль'
    return render_template('lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('user_name', None)
    return redirect('/lab4/login')


@lab4.route('/lab4/register', methods=['GET', 'POST'])
def register():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    if request.method == 'GET':
        return render_template('lab4/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    confirm = request.form.get('confirm_password')
    name = request.form.get('name')
    
    if not all([login, password, confirm, name]):
        return render_template('lab4/register.html', error='Все поля обязательны')
    
    if password != confirm:
        return render_template('lab4/register.html', error='Пароли не совпадают')
    
    if any(user['login'] == login for user in users):
        return render_template('lab4/register.html', error='Логин уже существует')
    
    users.append({
        'login': login,
        'password': password,
        'name': name,
        'gender': request.form.get('gender', 'не указан')
    })
    
    return render_template('lab4/register.html', success=f'Пользователь {name} зарегистрирован!')

@lab4.route('/lab4/users')
def users_list():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    safe_users = [{'login': u['login'], 'name': u['name'], 'gender': u.get('gender', 'не указан')} for u in users]
    return render_template('lab4/users.html', users=safe_users)

@lab4.route('/lab4/users/delete/<login>', methods=['POST'])
def delete_user(login):
    if 'login' not in session or session['login'] == login:
        return redirect('/lab4/users')
    
    global users
    users = [u for u in users if u['login'] != login]
    return redirect('/lab4/users')

@lab4.route('/lab4/users/edit/<login>', methods=['GET', 'POST'])
def edit_user(login):
    if 'login' not in session:
        return redirect('/lab4/login')
    
    user = next((u for u in users if u['login'] == login), None)
    if not user:
        return redirect('/lab4/users')
    
    if request.method == 'GET':
        return render_template('lab4/edit_user.html', user=user)
    
    new_login = request.form.get('login')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm = request.form.get('confirm_password')
    
    if not all([new_login, name]):
        return render_template('lab4/edit_user.html', user=user, error='Логин и имя обязательны')
    
    if new_login != login and any(u['login'] == new_login for u in users):
        return render_template('lab4/edit_user.html', user=user, error='Логин уже существует')
    
    if password and password != confirm:
        return render_template('lab4/edit_user.html', user=user, error='Пароли не совпадают')
    
    user['login'] = new_login
    user['name'] = name
    user['gender'] = request.form.get('gender', user.get('gender', 'не указан'))
    
    if password:
        user['password'] = password
    
    if session['login'] == login:
        session['login'] = new_login
        session['user_name'] = name
    
    return redirect('/lab4/users')


@lab4.route('/lab4/fridge', methods=['GET', 'POST'])
def fridge():
    if request.method == 'GET':
        error = session.pop('error', None)
        temperature = session.pop('temperature', None)
        snowflakes = session.pop('snowflakes', 0)
        message = session.pop('message', None)
        
        return render_template("lab4/fridge.html", error=error, temperature=temperature, snowflakes=snowflakes, message=message)
    
    temp_input = request.form.get('temperature')

    if not temp_input:
        session['error'] = "Ошибка: не задана температура"
        return redirect('/lab4/fridge')
    
    try:
        temperature = int(temp_input)
    except ValueError:
        session['error'] = "Ошибка: температура должна быть числом"
        return redirect('/lab4/fridge')

    if temperature < -12:
        session['error'] = "Не удалось установить температуру — слишком низкое значение"
    elif temperature > -1:
        session['error'] = "Не удалось установить температуру — слишком высокое значение"
    elif -12 <= temperature <= -9:
        session['message'] = f"Установлена температура: {temperature}°C"
        session['snowflakes'] = 3
        session['temperature'] = temperature
    elif -8 <= temperature <= -5:
        session['message'] = f"Установлена температура: {temperature}°C"
        session['snowflakes'] = 2
        session['temperature'] = temperature
    elif -4 <= temperature <= -1:
        session['message'] = f"Установлена температура: {temperature}°C"
        session['snowflakes'] = 1
        session['temperature'] = temperature
    
    return redirect('/lab4/fridge')

@lab4.route('/lab4/fridge/clear')
def fridge_clear():
    session.pop('error', None)
    session.pop('temperature', None)
    session.pop('snowflakes', None)
    session.pop('message', None)
    return redirect('/lab4/fridge')


@lab4.route('/lab4/grain', methods=['GET', 'POST'])
def grain():
    if request.method == 'GET':
        return render_template('lab4/grain.html')
    
    grain_type = request.form.get('grain_type')
    weight = request.form.get('weight')
    
    prices = {'barley': 12000, 'oats': 8500, 'wheat': 9000, 'rye': 15000}
    grain_names = {'barley': 'ячмень', 'oats': 'овёс', 'wheat': 'пшеница', 'rye': 'рожь'}
    
    if not grain_type:
        return render_template('lab4/grain.html', error='Выберите тип зерна')
    
    if not weight:
        return render_template('lab4/grain.html', error='Укажите вес')
    
    try:
        weight_float = float(weight)
    except ValueError:
        return render_template('lab4/grain.html', error='Вес должен быть числом')
    
    if weight_float <= 0:
        return render_template('lab4/grain.html', error='Вес должен быть положительным числом')
    
    if weight_float > 100:
        return render_template('lab4/grain.html', error='Такого объёма сейчас нет в наличии')
    
    price_per_ton = prices[grain_type]
    total_without_discount = weight_float * price_per_ton
    
    discount = 0
    discount_applied = False
    if weight_float > 10:
        discount = total_without_discount * 0.1
        total = total_without_discount - discount
        discount_applied = True
    else:
        total = total_without_discount
    
    grain_name = grain_names[grain_type]
    
    return render_template('lab4/grain.html', success=True, grain_name=grain_name, weight=weight_float,
                         total=total, discount=discount, discount_applied=discount_applied,
                         total_without_discount=total_without_discount, selected_grain=grain_type, entered_weight=weight)