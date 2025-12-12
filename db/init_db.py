from app import app, db
from db.models import users, articles  # Импорт моделей

with app.app_context():
    db.create_all()
    print("Таблицы созданы успешно!")
    