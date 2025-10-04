from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(pw: str) -> str:
    """
    Hash a password using the Argon2 password hashing algorithm.

        pw (str): The password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(pw)

def verify_password(pw: str, stored: str) -> bool:
    """
    Verify a password against a stored hashed password.

    Args:
        pw (str): The password to verify.
        stored (str): The stored hashed password.

    Returns:
        bool: Whether the password matches the stored hashed password.
    """
    return pwd_context.verify(pw, stored)
