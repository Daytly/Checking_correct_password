import random


def generate_key(length: int, collection: str) -> str:
    key = ''
    for _ in range(length):
        key += random.choice(collection)
    return key


def generate_unique_keys(count: int, length: int, collection: str) -> list:
    keys = set()
    while len(keys) < count:
        keys.add(generate_key(length, collection))
    return list(keys)


