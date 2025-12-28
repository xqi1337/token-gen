import random
import string

from typing import Tuple


class Utils:

    @staticmethod
    def random_password(length: int = 12) -> str:
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def random_string(length: int = 16) -> str:
        allowed_chars = string.ascii_lowercase + string.digits + "_."
        first_char = random.choice(string.ascii_lowercase + string.digits + "_")
        middle = ''.join(random.choice(allowed_chars) for _ in range(max(length - 2, 0)))
        last_char = random.choice(string.ascii_lowercase + string.digits + "_") if length > 1 else ""
        return first_char + middle + last_char

    @staticmethod
    def random_birthday():
        day = random.randint(1, 28)
        month = random.randint(1, 12)
        year = random.randint(1990, 2005)
        return year, month, day

    @staticmethod
    def load_proxy(file_path: str) -> str | None:
        with open(file_path, encoding="utf-8") as f:
            proxies = f.read().splitlines()

        if not proxies:
            return None

        proxy = random.choice(proxies)
        proxies.remove(proxy)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write("\n".join(proxies))

        return proxy
    