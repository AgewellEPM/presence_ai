from cryptography.fernet import Fernet
import os
import json
from virem_vault.key_derivation import derive_ephemeral_key

class VIREMVaultDriver:
    """
    ChaCha20 file-based vault for ephemeral, encrypted blocks.
    Designed for transient storage, with emphasis on encryption and decay.
    """
    def __init__(self, vault_path: str):
        self.vault_path = vault_path
        self.ephemeral_key = None # Key is derived per session or per block
        os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)
        print(f"VIREMVaultDriver initialized for persistent (encrypted) mode at: {self.vault_path}")

    def set_ephemeral_key(self, wakeword_hash: str, emotion_signature: str):
        """Derives and sets the ephemeral encryption key for the session."""
        self.ephemeral_key = derive_ephemeral_key(wakeword_hash, emotion_signature)
        print("Ephemeral key derived and set.")

    def _get_fernet(self):
        """Returns a Fernet instance using the current ephemeral key."""
        if not self.ephemeral_key:
            raise ValueError("Ephemeral key not set. Call set_ephemeral_key first.")
        return Fernet(self.ephemeral_key)

    def store_block(self, block_id: str, data: str):
        """
        Stores an encrypted data block.
        In a true ephemeral design, these blocks would have short lifespans
        or be overwritten frequently.
        """
        if not self.ephemeral_key:
            print("Warning: Attempted to store block without ephemeral key. Data not stored.")
            return

        f = self._get_fernet()
        encrypted_data = f.encrypt(data.encode('utf-8'))

        # Append to a file for simplicity. For robust design, manage blocks more carefully.
        with open(self.vault_path, 'ab') as vault_file:
            vault_file.write(b'--BLOCK_START--\n')
            vault_file.write(block_id.encode('utf-8') + b'\n')
            vault_file.write(encrypted_data + b'\n')
            vault_file.write(b'--BLOCK_END--\n')
        print(f"Block '{block_id}' encrypted and stored.")

    def retrieve_block(self, block_id: str) -> str | None:
        """
        Retrieves and decrypts a specific data block.
        This is primarily for demonstration; in a truly ephemeral system,
        retrieval might be highly restricted or time-bound.
        """
        if not self.ephemeral_key:
            print("Warning: Attempted to retrieve block without ephemeral key. Cannot retrieve.")
            return None

        f = self._get_fernet()
        try:
            with open(self.vault_path, 'rb') as vault_file:
                content = vault_file.read()
                blocks = content.split(b'--BLOCK_START--\n')
                for block in blocks[1:]: # Skip initial empty split
                    if block_id.encode('utf-8') in block:
                        parts = block.split(b'\n')
                        if len(parts) >= 3:
                            encrypted_data = parts[1] # Assumes ID is on line 0, data on line 1 of block content
                            # Simple regex for block_id in content, more robust parsing needed for actual implementation
                            try:
                                decrypted_data = f.decrypt(encrypted_data).decode('utf-8')
                                print(f"Block '{block_id}' retrieved and decrypted.")
                                return decrypted_data
                            except Exception as e:
                                print(f"Error decrypting block '{block_id}': {e}")
                                return None
        except FileNotFoundError:
            print("Vault file not found.")
            return None
        print(f"Block '{block_id}' not found.")
        return None

    def clear_vault(self):
        """
        Clears the persistent vault file. This would be part of a
        session termination or decay mechanism.
        """
        if os.path.exists(self.vault_path):
            os.remove(self.vault_path)
            print("VIREM Vault file cleared.")
        self.ephemeral_key = None # Clear key on vault clear
