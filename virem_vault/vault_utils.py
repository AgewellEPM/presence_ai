# presence_ai/virem_vault/vault_utils.py

from cryptography.fernet import Fernet

def generate_key():
    """Generate a new Fernet key."""
    return Fernet.generate_key()

def encrypt_data(data: bytes, key: bytes) -> bytes:
    fernet = Fernet(key)
    return fernet.encrypt(data)

def decrypt_data(token: bytes, key: bytes) -> bytes:
    fernet = Fernet(key)
    return fernet.decrypt(token)
