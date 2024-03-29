from flask import Flask, render_template, redirect, make_response, jsonify, url_for, request

from data import db_session
from data.codes import Codes
from data.keys import Keys
from forms.InputCodeAndKeyForm import InputCodeAndKeyForm
from forms.InputCodeForm import InputCodeForm

def update_no_use_codes(count: int):
    db_sess = db_session.create_session()
    rows = db_sess.query(Codes).filter(Codes.is_use == False)[:count]
    return rows

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db_session.global_init("db/db.db")
no_use_codes = []


def main():
    global no_use_codes
    no_use_codes = update_no_use_codes(10)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template("index.html")


@app.route("/codes/", methods=['GET', 'POST'])
def input_code_and_kay():
    key = request.args.get('key')
    if key is None:
        form = InputCodeAndKeyForm()
        is_input_key = False
    else:
        form = InputCodeForm()
        is_input_key = True
    message = ""
    if form.validate_on_submit():
        if key is None:
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
                           is_input_key=is_input_key,
                           codes=no_use_codes,
                           url='/codes/')


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


def check_correct_key(key):
    db_sess = db_session.create_session()
    row = db_sess.get(Keys, key)
    db_sess.close()
    if row is None:
        return False
    if row.is_use:
        return False
    return True


def check_correct_code(code):
    db_sess = db_session.create_session()
    row = db_sess.get(Codes, code)
    db_sess.close()
    if row is None:
        return False
    if row.is_use:
        return False
    return True


def save_code_in_db(code):
    global no_use_codes
    db_sess = db_session.create_session()
    row = db_sess.get(Codes, code)
    if row is not None:
        row.is_use = True
        db_sess.merge(row)
        db_sess.commit()
        db_sess.close()
        no_use_codes = update_no_use_codes(10)
        return True
    return False



def use_key(key):
    db_sess = db_session.create_session()
    row = db_sess.get(Keys, key)
    if row is not None:
        row.is_use = True
        db_sess.merge(row)
        db_sess.commit()
        db_sess.close()
        return True
    db_sess.close()
    return False


if __name__ == '__main__':
    main()
