import jwt
import uuid
import logging
from itsdangerous import BadSignature, URLSafeTimedSerializer
from passlib.context import CryptContext
from datetime import timedelta, datetime
from src.config import config

# Use Argon2 instead of bcrypt
passwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


ACCESS_TOKEN_EXPIRY = 3600


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


def create_access_token(user_data : dict, expiry : timedelta = None, refresh: bool = False):
    payload = {}
     
    payload['jti'] = str(uuid.uuid4())
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['refresh'] = refresh
    
    token = jwt.encode(
        payload=payload,
        key=config.JWT_SECRET,
        algorithm=config.JWT_ALGORITHM
    )
    
    return token


def decode_token(token : str) -> dict:
    try:
        token_data = jwt.decode(
        jwt=token,
        key=config.JWT_SECRET,
        algorithms=config.JWT_ALGORITHM
        )
    
        return token_data
    
    except jwt.PyJWKError as e:
        logging.exception(e)
        return None
    
    

serializer = URLSafeTimedSerializer(secret_key=config.JWT_SECRET, salt="email-password-reset")



def create_url_safe_token(data: dict):
    """
    Create a URL-safe token for email/password reset
    """
    try:
        return serializer.dumps(data)
    except Exception as e:
        logging.error(f"Token creation failed: {e}")
        

def decode_url_safe_token(token:str, max_age: int = 3600):
    """
    Validate & decode token safely
    """
    try:
        token_data = serializer.loads(token)

        return token_data
    
    except Exception as e:
        logging.error(str(e))

