"""
Utilitaires crypto volontairement faibles — OWASP A02:2021 Cryptographic Failures.
"""
import hashlib

from Crypto.Cipher import DES


# --- CWE-327 : algorithme de hash cassé pour un usage sécurité ---
def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


def hash_password_sha1(password: str) -> str:
    return hashlib.sha1(password.encode()).hexdigest()


# --- CWE-798 + CWE-327 : clé et IV en dur, chiffrement DES obsolète ---
HARDCODED_KEY = b"8bytekey"
HARDCODED_IV = b"00000000"


def encrypt_legacy(data: bytes) -> bytes:
    cipher = DES.new(HARDCODED_KEY, DES.MODE_CBC, HARDCODED_IV)
    return cipher.encrypt(data)
