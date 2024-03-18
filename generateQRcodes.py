import qrcode
from tinydb import TinyDB

if input("Введите пароль: ") == "HardPassword":
    small_db = TinyDB('keys_db.json')
    table = small_db.table("checks")
    keys = [i["key"] for i in table.all()]
    for i in range(len(keys[:300])):
        URL = "http://" + "127.0.0.1:5000" + f"/codes/{keys[i]}"
        filename = f"QRs/QR{i}.png"
        img = qrcode.make(URL)
        img.save(filename)
    small_db.close()
