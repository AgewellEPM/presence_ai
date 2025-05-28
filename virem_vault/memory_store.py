# This file can act as a unified interface to either driver.py or scratchpad.py
# Or, its logic can be absorbed into run_demo.py as done above for simplicity.
# For a more complex system, this would manage block types, indices, etc.

class MemoryStore:
    def __init__(self, vault_instance):
        self.vault = vault_instance
        print(f"MemoryStore initialized with {type(vault_instance).__name__}.")

    def write_data(self, key: str, value: str):
        self.vault.store_block(key, value)

    def read_data(self, key: str) -> str | None:
        return self.vault.retrieve_block(key)

    def clear_all(self):
        if hasattr(self.vault, 'clear_session_memory'):
            self.vault.clear_session_memory()
        elif hasattr(self.vault, 'clear_vault'):
            self.vault.clear_vault()
