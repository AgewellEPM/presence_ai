class EmotionDecayEngine:
    def __init__(self, decay_rate: float = 0.05):
        self.decay_rate = decay_rate
        print(f"EmotionDecayEngine initialized with decay rate: {self.decay_rate}")

    def apply_decay(self, weights: dict) -> dict:
        """
        Gradually reduces emotion pathway weights over time,
        unless reinforced by new emotional resonance.
        This helps the AI return to a neutral state and prevents
        permanent biases.
        """
        decayed_weights = {}
        for emotion, weight in weights.items():
            # Apply decay, ensuring weight doesn't go below a minimum (e.g., 0.1 for neutrality)
            decayed_weights[emotion] = max(0.1, weight - self.decay_rate)
        return decayed_weights
