from constants import collection
from data import db_session
from data.keys import Keys
from data.keysOld import KeysOld
from functions import generate_unique_keys

if input("Введите пароль: ") == "HardPassword":
    db_session.global_init("db/db.db")
    db_sess = db_session.create_session()
    db_sess.query(KeysOld).delete()
    db_sess.commit()
    new = []
    for oldKey in db_sess.query(Keys).all():
        new = Keys()
        new.key = oldKey.key
        new.is_use = oldKey.is_use
    db_sess.bulk_save_objects(new)
    db_sess.commit()
    db_sess.query(Keys).delete()
    for key in generate_unique_keys(5000, 30, collection):
        new_key = Keys()
        new_key.key = key
        db_sess.merge(new_key)
    db_sess.commit()
    db_sess.close()
else:
    print("В доступе отказано")
