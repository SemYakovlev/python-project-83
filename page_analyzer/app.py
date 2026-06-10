import os
import validators
import requests
from requests.exceptions import RequestException
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
from urllib.parse import urlparse

from page_analyzer import db
from page_analyzer.parser import parse_html

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


def validate_url(url):
    errors = []
    if not url:
        errors.append('URL обязателен')
    elif not validators.url(url) or len(url) > 255:
        errors.append("Некорректный URL")
    return errors


@app.route('/')
def index():
    return render_template('index.html')


@app.post('/urls')
def url_post():
    url = request.form.get('url')
    errors = validate_url(url)

    if errors:
        flash(errors[0], 'danger')
        return render_template('index.html', url=url, errors=errors), 422

    parsed_url = urlparse(url)
    normalize_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    url_exists = db.get_url_by_name(normalize_url)

    if url_exists:
        flash('Страница уже существует', 'info')
        url_id = url_exists[0]
    else:
        url_id = db.add_url(normalize_url)
        flash('Страница успешно добавлена', 'success')

    return redirect(url_for('show_url', id=url_id))


@app.route('/urls')
def urls_get():
    urls = db.get_urls()
    return render_template('urls.html', urls=urls)


@app.post('/urls/<int:id>/checks')
def check_url(id):
    url_data = db.get_url_by_id(id)
    if not url_data:
        return render_template('errors/404.html'), 404
    url_name = url_data[1]

    try:
        response = requests.get(url_name, timeout=5)
        response.raise_for_status()
        status_code = response.status_code

        h1, title, description = parse_html(response.text)


        db.add_check(id, status_code, h1, title, description)
        flash('Страница успешно проверена', 'success')

    except RequestException:
        flash('Произошла ошибка при проверке', 'danger')

    return redirect(url_for('show_url', id=id))


@app.route('/urls/<int:id>')
def show_url(id):
    url_data = db.get_url_by_id(id)

    if not url_data:
        return render_template('errors/404.html'), 404

    url_dict = {
        'id': url_data[0],
        'name': url_data[1],
        'created_at': url_data[2]
    }
    checks = db.get_checks(id)

    return render_template('url_detail.html', url=url_dict, checks=checks)