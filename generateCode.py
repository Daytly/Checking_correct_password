from tinydb import TinyDB

from constants import collection
from functions import generate_unique_keys

if input("Введите пароль: ") == "HardPassword":
    small_db = TinyDB('keys_db.json')
    table = small_db.table("codes")
    small_db.drop_table("codes")
    for code in range(1, 3001):
        table.insert({"code": code, "isCheck": False})
    small_db.close()
