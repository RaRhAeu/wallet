import hashlib
import hmac
import bcrypt
from Crypto.Cipher import AES
from base64 import b64decode, b64encode

from wallet.settings import settings


def generate_password_hash(text: str) -> str:
    # bcrypt.gensalt() uses os.urandom and has 12 rounds set by default
    hashed = bcrypt.hashpw(text.encode("utf-8"), bcrypt.gensalt())
    return hashed.decode("utf-8")


def verify_password(plaintext: str, hashed: str):
    return bcrypt.checkpw(plaintext.encode("utf-8"), hashed.encode("utf-8"))


def generate_aes_key_from_hash(password: str) -> bytes:
    m = hashlib.md5()
    m.update(password.encode("utf-8"))
    return m.digest()


def aes_encrypt(key: bytes, data: str) -> str:
    cipher = AES.new(
            key, AES.MODE_CFB, IV=b64decode(settings.AES_IV)
        )
    return b64encode(cipher.encrypt(data.encode("utf-8"))).decode("utf-8")


def aes_decrypt(key: bytes, data: str) -> str:
    cipher = AES.new(
            key, AES.MODE_CFB, IV=b64decode(settings.AES_IV)
        )
    return cipher.decrypt(b64decode(data.encode("utf-8"))).decode("utf-8")


def safe_compare(string1, string2) -> bool:
    s1 = str(string1).encode("utf-8")
    s2 = str(string2).encode("utf-8")
    return hmac.compare_digest(s1, s2)