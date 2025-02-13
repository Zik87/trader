import json
import sqlite3
import os
from cryptography.fernet import Fernet

# Генерация и сохранение ключа шифрования
def generate_encryption_key():
    key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(key)
    return key

# Загрузка ключа шифрования
def load_encryption_key():
    return open("encryption_key.key", "rb").read()

# Шифрование данных
def encrypt_data(data, key):
    f = Fernet(key)
    encrypted_data = f.encrypt(data.encode())
    return encrypted_data

# Создание базы данных и таблицы
def create_database():
    conn = sqlite3.connect('keys.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS encrypted_keys
                 (account TEXT, encrypted_key BLOB)''')
    conn.commit()
    conn.close()

# Сохранение зашифрованных ключей в базу данных
def save_encrypted_keys(encrypted_keys):
    conn = sqlite3.connect('keys.db')
    c = conn.cursor()
    for account, encrypted_key in encrypted_keys.items():
        c.execute("INSERT INTO encrypted_keys VALUES (?, ?)", (account, encrypted_key))
    conn.commit()
    conn.close()

# Основная функция
def main():
    # Генерация или загрузка ключа шифрования
    if not os.path.exists("encryption_key.key"):
        key = generate_encryption_key()
    else:
        key = load_encryption_key()

    # Загрузка приватных ключей из файла
    with open('private_keys.txt', 'r') as file:
        private_keys = json.load(file)

    # Шифрование приватных ключей
    encrypted_keys = {}
    for account, private_key in private_keys.items():
        encrypted_keys[account] = encrypt_data(private_key, key)

    # Создание базы данных и сохранение зашифрованных ключей
    create_database()
    save_encrypted_keys(encrypted_keys)

    # Удаление исходного файла с приватными ключами
    os.remove('private_keys.txt')

if __name__ == "__main__":
    main()
