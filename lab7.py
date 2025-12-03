from flask import Blueprint, url_for, request, render_template, make_response, redirect, session, current_app


lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7.index.html')


films = [
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": 
    }


]