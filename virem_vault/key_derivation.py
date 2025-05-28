import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend

def derive_ephemeral_key(wakeword_hash: str, emotion_signature: str) -> bytes:
    """
    Derives an ephemeral encryption key using a combination of a
    wakeword hash (user-specific, but transient) and an emotional signature
    (AI's current affective state).

    This key is designed to be short-lived and non-reproducible across sessions
    or even between different emotional states.
    """
    # Combine the inputs into a single "password"
    password_bytes = (wakeword_hash + emotion_signature).encode('utf-8')

    # Use a fixed, public salt for deterministic key derivation within a session,
    # or generate a random salt per derivation for higher security if the salt
    # can be securely transmitted/discarded. For ephemeral keys, a fixed salt
    # can be acceptable if the inputs (wakeword_hash, emotion_signature) are
    # sufficiently dynamic and never stored.
    salt = b'presence_ai_ephemeral_salt' # In a real system, this might be dynamically generated and discarded

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, # For AES256, Fernet expects 32 bytes
        salt=salt,
        iterations=100000, # Sufficient iterations for key stretching
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
    return key
