from data import db_session
from data.codes import Codes

if input("Введите пароль: ") == "HardPassword":
    db_session.global_init("db/db.db")
    db_sess = db_session.create_session()
    db_sess.query(Codes).delete()
    for code in range(1, 3001):
        new_code = Codes()
        new_code.code = code
        db_sess.merge(new_code)
    db_sess.commit()
    db_sess.close()
else:
    print("В доступе отказано")
