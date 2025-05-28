# presence_ai/config/config.py
import os
import json

class Config:
    _instance = None # Singleton instance

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = os.path.join(os.path.dirname(__file__), 'config.json')
        try:
            with open(config_path, 'r') as f:
                json_config = json.load(f)

            self.DEFAULT_MODE = json_config.get("default_mode", "scratch")
            self.VAULT_KEY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), json_config.get("vault_key_path", "config/vault.key"))
            self.EMOTION_LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), json_config.get("emotion_log_file", "logs/ere_weight_log.jsonl"))

            # Ensure directories exist
            os.makedirs(os.path.dirname(self.VAULT_KEY_PATH), exist_ok=True)
            os.makedirs(os.path.dirname(self.EMOTION_LOG_FILE), exist_ok=True)

        except FileNotFoundError:
            print(f"Error: config.json not found at {config_path}. Using default settings.")
            self.DEFAULT_MODE = "scratch"
            self.VAULT_KEY_PATH = os.path.join(os.getcwd(), "config", "vault.key")
            self.EMOTION_LOG_FILE = os.path.join(os.getcwd(), "logs", "ere_weight_log.jsonl")

        self.DEFAULT_DECAY_RATE = 0.05
        self.INITIAL_PATHWAY_WEIGHTS = {
            "joy": 0.5, "rage": 0.5, "calm": 0.5, "sacred": 0.5, "neutral": 1.0 # Updated emotions
        }
        # Add other configurable parameters here
