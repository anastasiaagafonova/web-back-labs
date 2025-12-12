# init_db.py
import sys
import os

# Указываем путь к проекту
project_path = '/home/Aanastasi8/web-back-labs'
sys.path.insert(0, project_path)
os.chdir(project_path)

# Импортируем из твоего app.py
from app import app
from db import db
from db.models import users, articles

print("🚀 Начинаю создание таблиц...")
print(f"📁 Путь: {project_path}")
print(f"🔗 База данных: {app.config.get('SQLALCHEMY_DATABASE_URI')}")

# ВАЖНО: Используем контекст приложения
with app.app_context():
    try:
        # Принудительно инициализируем связь
        db.init_app(app)  # Еще раз на всякий случай
        
        # Создаем таблицы
        db.create_all()
        
        print("✅ УСПЕХ! Таблицы созданы!")
        
        # Проверяем
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"📊 Созданные таблицы: {tables}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()