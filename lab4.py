from flask import Blueprint, redirect, url_for, render_template
lab2 = Blueprint('lab4', __name__)


@lab3.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')
