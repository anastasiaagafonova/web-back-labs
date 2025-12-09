from flask import Blueprint, url_for, request, render_template, make_response, redirect, session, current_app, abort, jsonify
from datetime import datetime
import sqlite3
from pathlib import Path

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/index.html')

@lab8.route('/lab8/login')

@lab8.route('/lab8/register')

@lab8.route('/lab8/articles')

@lab8.route('/lab8/create')