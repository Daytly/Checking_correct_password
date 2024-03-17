import os
from flask import Flask, render_template, redirect, make_response, request, abort, jsonify, url_for
from tinydb import TinyDB, Query

from constants import collection
from forms.InputCodeAndKeyForm import InputCodeAndKeyForm
from forms.InputCodeForm import InputCodeForm
from functions import generate_unique_keys

small_db = TinyDB('keys_db.json')
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


def main():
    app.run()


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


def check_correct_key(key):
    table = small_db.table("checks")
    Todo = Query()
    is_check = table.get(Todo.key == key)
    if is_check is None:
        return False
    if is_check["isCheck"]:
        return False
    return True


def check_correct_code(code):
    table = small_db.table("codes")
    Todo = Query()
    raw_code = table.get(Todo.code == code)
    if raw_code is None:
        return True
    return False


def save_code_in_db(code):
    table = small_db.table("codes")
    table.insert({"code": code})
    return True


def use_key(key):
    table_keys = small_db.table("checks")
    Todo = Query()
    is_check = table_keys.get(Todo.key == key)
    if is_check is not None:
        is_check["isCheck"] = True
        table_keys.update(is_check, Todo.key == key)
        return True
    return False


@app.route("/codes/<string:key>", methods=['GET', 'POST'])
def input_code(key):
    form = InputCodeForm()
    message = ""
    if form.validate_on_submit():
        if check_correct_key(key):
            if check_correct_code(form.inputCode.data):
                if save_code_in_db(form.inputCode.data):
                    if use_key(key):
                        return redirect(f'/success/{form.inputCode.data}')
                else:
                    message = "Ошибка"
            else:
                message = "Такой код уже был"
        else:
            message = "Неверный ключ"
    return render_template('codes.html', form=form, url_for=url_for, message=message,
                           is_input_key=True,
                           url=f'/codes/{key}')


@app.route("/codes/", methods=['GET', 'POST'])
def input_code_and_kay():
    form = InputCodeAndKeyForm()
    message = ""
    if form.validate_on_submit():
        key = form.inputKey.data
        if check_correct_key(key):
            if check_correct_code(form.inputCode.data):
                if save_code_in_db(form.inputCode.data):
                    if use_key(key):
                        return redirect(f'/success/{form.inputCode.data}')
                else:
                    message = "Ошибка"
            else:
                message = "Такой код уже был"
        else:
            message = "Неверный ключ"
    return render_template('codes.html', form=form, url_for=url_for, message=message,
                           is_input_key=False,
                           url=f'/codes/')


@app.route("/success/<int:code>")
def success(code):
    return render_template('success.html',
                           code=code,
                           url_for=url_for)


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(_):
    return make_response(jsonify({'error': 'Bad Request'}), 400)


if __name__ == '__main__':
    main()
