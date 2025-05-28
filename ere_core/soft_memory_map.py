import json
import os
from config.config import Config

class SoftMemoryMap:
    def __init__(self):
        self.log_file = Config().LOG_PATH
        os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
        print(f"SoftMemoryMap logging to: {self.log_file}")

    def log_weights(self, weights: dict):
        """Logs the current state of pathway weights to a file."""
        log_entry = {
            "timestamp": os.urandom(8).hex(), # Use a non-time-based ID for privacy/statelessness, or just remove if not needed for specific tracking
            "weights": weights
        }
        with open(self.log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')

    def get_bias_trends(self):
        """
        Analyzes the log file to understand long-term emotional bias trends.
        This would be used for internal analysis/tuning, not user data recall.
        """
        trends = {}
        try:
            with open(self.log_file, 'r') as f:
                for line in f:
                    entry = json.loads(line)
                    for emotion, weight in entry['weights'].items():
                        if emotion not in trends:
                            trends[emotion] = []
                        trends[emotion].append(weight)
        except FileNotFoundError:
            print("Soft memory log file not found. No trends to analyze.")
        return trends
