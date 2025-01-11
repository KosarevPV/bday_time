"""
Инструменты для аутентификации.
"""

__author__ = "pv.kosarev"

import hashlib
import hmac
import secrets
import string


def generate_hmac_sha256(message: str, key: str) -> str:
    """
    Генерирует HMAC-SHA256 для заданного ключа и сообщения.

    :param key: Ключ для генерации HMAC-SHA256.
    :param message: Сообщение, для которого нужно сгенерировать HMAC-SHA256.
    :return: Значение HMAC-SHA256 в виде шестнадцатеричной строки (len(64)).
    """
    bytes_key = key.encode("utf-8")
    bytes_message = message.encode("utf-8")
    hmac_obj = hmac.new(bytes_key, bytes_message, hashlib.sha256)

    return hmac_obj.hexdigest()


def generate_api_key(length: int = 64) -> str:
    """
    Генерирует случайный API ключ указанной длины.

    :param length: Длина генерируемого API ключа. По умолчанию 64.
    :return: Сгенерированный API ключ.
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    api_key = "".join(secrets.choice(alphabet) for _ in range(length))

    return api_key


if __name__ == "__main__":
    api_key = generate_api_key()
    hmac_api_key = generate_hmac_sha256(api_key, key="")
    print(api_key, hmac_api_key, sep="\n")
