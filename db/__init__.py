from flask_sqlalchemy import SQLAlchemy
from .models import users, articles

db = SQLAlchemy()

__all__ = ['db', 'users', 'articles']