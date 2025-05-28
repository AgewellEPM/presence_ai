import os

class Config:
    def __init__(self):
        self.VAULT_PATH = os.path.join(os.getcwd(), "vault_data", "virem_vault.enc")
        self.LOG_PATH = os.path.join(os.getcwd(), "logs", "ere_weight_log.jsonl")
        self.DEFAULT_DECAY_RATE = 0.05 # For emotion_decay_engine
        self.INITIAL_PATHWAY_WEIGHTS = {
            "joy": 0.5, "sadness": 0.5, "anger": 0.5, "confusion": 0.5, "neutral": 1.0
        }
        # Add other configurable parameters here
