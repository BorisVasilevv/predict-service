import secrets

# Генерация случайного секретного ключа
print(secrets.token_hex(32))  # 32 байта -> 64-символьная шестнадцатеричная строка