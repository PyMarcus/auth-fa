from passlib.context import CryptContext

CRYPTO: CryptContext = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hash_password: str) -> bool:
    """
    Check if the provided plaintext password matches the hashed password stored in the database.
    Args:
        password (str): The plaintext password input by the user.
        hash_password (str): The hashed password stored in the database.
    Returns:
        bool: True if the password matches the hash, False otherwise.
    """
    return CRYPTO.verify(password, hash_password)


def create_hash(password: str) -> str:
    """
    Create a hash to the password received
    Args:
        password (str): The plaintext password input by the user.
    Returns:
        hash_password (str): The hashed password
    """
    return CRYPTO.hash(password)
