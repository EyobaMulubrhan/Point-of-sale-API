import hashlib
import hmac
import secrets

_ITERATIONS = 390_000
_ALGO = "sha256"


def hash_password(password: str) -> str:

    salt = secrets.token_hex(16)
    derived = hashlib.pbkdf2_hmac(_ALGO, password.encode("utf-8"), bytes.fromhex(salt), _ITERATIONS)
    return f"pbkdf2_sha256${_ITERATIONS}${salt}${derived.hex()}"


def verify_password(password: str, password_hash: str) -> bool:
   
    try:
        algo, iterations, salt, hash_hex = password_hash.split("$")
        if algo != "pbkdf2_sha256":
            return False
        iterations = int(iterations)
    except (ValueError, AttributeError):
        return False

    derived = hashlib.pbkdf2_hmac(_ALGO, password.encode("utf-8"), bytes.fromhex(salt), iterations)
    return hmac.compare_digest(derived.hex(), hash_hex)