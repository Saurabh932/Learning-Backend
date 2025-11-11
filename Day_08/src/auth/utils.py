from passlib.context import CryptContext

# Use Argon2 instead of bcrypt
passwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)

def generate_passwd_hash(password: str) -> str:
    """
    Hash a plain-text password using Argon2 algorithm.
    """
    if not isinstance(password, str):
        raise TypeError(f"Password must be a string, got {type(password)}")

    return passwd_context.hash(password)

def verify_passwd(password: str, hash: str) -> bool:
    """
    Verify a plain-text password against its Argon2 hash.
    """
    return passwd_context.verify(password, hash)
