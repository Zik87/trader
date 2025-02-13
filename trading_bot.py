import sqlite3
from cryptography.fernet import Fernet

# Загрузка ключа шифрования
def load_encryption_key():
    return open("encryption_key.key", "rb").read()

# Расшифровка данных
def decrypt_data(encrypted_data, key):
    f = Fernet(key)
    decrypted_data = f.decrypt(encrypted_data).decode()
    return decrypted_data

# Загрузка зашифрованных ключей из базы данных
def load_encrypted_keys():
    conn = sqlite3.connect('keys.db')
    c = conn.cursor()
    c.execute("SELECT * FROM encrypted_keys")
    encrypted_keys = c.fetchall()
    conn.close()
    return encrypted_keys

# Основная функция
def main():
    # Загрузка ключа шифрования
    key = load_encryption_key()

    # Загрузка зашифрованных ключей
    encrypted_keys = load_encrypted_keys()

    # Расшифровка приватных ключей
    private_keys = {}
    for account, encrypted_key in encrypted_keys:
        private_keys[account] = decrypt_data(encrypted_key, key)

    # Здесь добавьте логику вашего торгового бота, используя приватные ключи
    for account, private_key in private_keys.items():
        print(f"Account: {account}, Private Key: {private_key}")
        # Добавьте код для торговли

if __name__ == "__main__":
    main()
