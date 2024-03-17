from tinydb import TinyDB

from constants import collection
from functions import generate_unique_keys

if input("Введите пароль: ") == "HardPassword":
    small_db = TinyDB('keys_db.json')
    table = small_db.table("checks")
    small_db.drop_table("checks_old")
    table1 = small_db.table("checks_old")
    for row in table.all():
        table1.insert(row)
    small_db.drop_table("checks")
    for key in generate_unique_keys(5000, 30, collection):
        table.insert({"key": key, "isCheck": False})
    small_db.close()
