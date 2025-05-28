# presence_ai/virem_vault/vault_block_filter.py

from typing import Dict, Any

class VaultBlockFilter:
    def __init__(self, config_thresholds: Dict[str, Any] = None):
        """
        Initializes the VaultBlockFilter with emotional thresholds for storage.
        These thresholds determine when a memory block is deemed 'significant' enough to persist.
        :param config_thresholds: Optional dictionary of specific thresholds to override defaults.
        """
        # Define filtering rules/thresholds. These can be made configurable via config.json later.
        # Example rule: a "soul moment" is when both 'sacred' and 'joy' are above certain weights.
        self.thresholds = {
            "sacred_joy_combined_threshold": 0.7, # Combined sum of weights for a 'soul moment'
            "min_individual_weight_for_soul_moment": 0.4 # Minimum individual weight for each emotion to qualify
            # Add other specific emotional thresholds for persistence here if needed, e.g.:
            # "extreme_rage_threshold": 0.95
        }
        if config_thresholds:
            self.thresholds.update(config_thresholds) # Allow overriding via constructor if desired

        print("VaultBlockFilter initialized with emotional thresholds.")
        print(f"Current thresholds: {self.thresholds}")

    def should_store_block(self, ere_pathway_weights: Dict[str, float]) -> bool:
        """
        Determines if a memory block should be stored in the persistent vault
        based on the current emotional state (ERE pathway weights).

        This example primarily checks for a "soul moment" defined by high 'sacred' and 'joy' weights.
        :param ere_pathway_weights: The current dictionary of ERE pathway weights.
        :return: True if the block should be stored, False otherwise.
        """
        sacred_weight = ere_pathway_weights.get("sacred", 0.0)
        joy_weight = ere_pathway_weights.get("joy", 0.0)

        # Condition 1: Check for a "soul moment"
        # Requires both 'sacred' and 'joy' to individually meet a minimum,
        # AND their combined sum to meet a higher threshold.
        is_soul_moment = (
            sacred_weight >= self.thresholds["min_individual_weight_for_soul_moment"] and
            joy_weight >= self.thresholds["min_individual_weight_for_soul_moment"] and
            (sacred_weight + joy_weight) >= self.thresholds["sacred_joy_combined_threshold"]
        )

        if is_soul_moment:
            print(f"VaultBlockFilter: 'Soul Moment' detected! (Sacred: {sacred_weight:.2f}, Joy: {joy_weight:.2f}). Block will be stored.")
            return True
        else:
            # You can add other specific conditions for persistence here, e.g., if a single emotion
            # reaches an extreme threshold (e.g., self.thresholds.get("extreme_rage_threshold", 1.0) <= ere_pathway_weights.get("rage", 0.0)).
            # For this filter, the default is to NOT store unless a specific condition is met.
            # print(f"VaultBlockFilter: No 'Soul Moment' detected. (Sacred: {sacred_weight:.2f}, Joy: {joy_weight:.2f}). Block not stored.") # Uncomment for verbose debug
            return False
