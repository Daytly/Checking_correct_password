import qrcode

from data import db_session
from data.keys import Keys

if input("Введите пароль: ") == "HardPassword":
    db_session.global_init("db/db.db")
    db_sess = db_session.create_session()
    keys = db_sess.query(Keys).all()[:300]
    for i in range(len(keys)):
        URL = "https://" + "super-c0mputer.glitch.me" + f"/codes/{keys[i].key}"
        filename = f"QRs/QR{i}.png"
        img = qrcode.make(URL)
        img.save(filename)
    db_sess.close()
else:
    print("В доступе отказано")
