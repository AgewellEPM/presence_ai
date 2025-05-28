class ScratchpadVault:
    """
    RAM-only memory vault for true stateless operation.
    No data is ever written to disk.
    """
    def __init__(self):
        self._memory_store = {} # In-memory dictionary
        print("ScratchpadVault initialized (RAM-only).")

    def store_block(self, block_id: str, data: str):
        """Stores a data block temporarily in RAM."""
        self._memory_store[block_id] = data
        print(f"Block '{block_id}' stored in RAM scratchpad.")

    def retrieve_block(self, block_id: str) -> str | None:
        """Retrieves a data block from RAM."""
        return self._memory_store.get(block_id)

    def clear_session_memory(self):
        """Clears all data from the RAM scratchpad."""
        self._memory_store.clear()
        print("ScratchpadVault: All RAM memory cleared.")
