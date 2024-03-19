from flask import Flask, render_template, redirect, make_response, jsonify, url_for

from data import db_session
from data.codes import Codes
from data.keys import Keys
from forms.InputCodeAndKeyForm import InputCodeAndKeyForm
from forms.InputCodeForm import InputCodeForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'

no_use_codes = []


def main():
    global no_use_codes
    db_session.global_init("db/db.db")
    no_use_codes = update_no_use_codes(10)
    app.run()


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


def check_correct_key(key):
    db_sess = db_session.create_session()
    row = db_sess.query(Keys).get(key)
    db_sess.close()
    if row is None:
        return False
    if row.is_use:
        return False
    return True


def check_correct_code(code):
    db_sess = db_session.create_session()
    row = db_sess.query(Codes).get(code)
    db_sess.close()
    if row is None:
        return False
    if row.is_use:
        return False
    return True


def save_code_in_db(code):
    global no_use_codes
    db_sess = db_session.create_session()
    row = db_sess.query(Codes).get(code)
    if row is not None:
        row.is_use = True
        db_sess.merge(row)
        db_sess.commit()
        db_sess.close()
        no_use_codes = update_no_use_codes(10)
        return True
    return False


def update_no_use_codes(count: int):
    db_sess = db_session.create_session()
    rows = db_sess.query(Codes).filter(Codes.is_use == False)[:count]
    return rows


def use_key(key):
    db_sess = db_session.create_session()
    row = db_sess.query(Keys).get(key)
    if row is not None:
        row.is_use = True
        db_sess.merge(row)
        db_sess.commit()
        db_sess.close()
        return True
    db_sess.close()
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
                           codes=no_use_codes,
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
                           codes=no_use_codes,
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
