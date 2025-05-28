from ere_core.soft_memory_map import SoftMemoryMap
from ere_core.emotion_decay_engine import EmotionDecayEngine
from ere_core.presence_persona import PresencePersona
from config.config import Config
import random

class EREEngine:
    def __init__(self):
        self.config = Config()
        self.pathway_weights = self.config.INITIAL_PATHWAY_WEIGHTS.copy()
        self.soft_memory_map = SoftMemoryMap()
        self.decay_engine = EmotionDecayEngine(decay_rate=self.config.DEFAULT_DECAY_RATE)
        self.presence_persona = PresencePersona()
        print("EREEngine initialized with default pathway weights.")

    def detect_emotion(self, text: str) -> str:
        """
        Mocks emotion detection from user input.
        In a real system, this would use NLP models (e.g., sentiment analysis, emotion recognition).
        """
        # Simple keyword-based or random emotion detection for demo
        text_lower = text.lower()
        if "happy" in text_lower or "joy" in text_lower:
            return "joy"
        elif "sad" in text_lower or "unhappy" in text_lower:
            return "sadness"
        elif "angry" in text_lower or "frustrated" in text_lower:
            return "anger"
        elif "confused" in text_lower or "huh" in text_lower or "what" in text_lower:
            return "confusion"
        else:
            return random.choice(["joy", "sadness", "anger", "confusion", "neutral"]) # Random for demo

    def adjust_pathway_weights(self, detected_emotion: str, intensity: float = 0.1):
        """
        Adjusts internal pathway weights based on detected emotion.
        This is the core of the "soft memory" learning.
        Weights reflect the AI's predisposition to respond in certain ways.
        """
        if detected_emotion in self.pathway_weights:
            # Increase weight for the detected emotion
            self.pathway_weights[detected_emotion] = min(1.0, self.pathway_weights[detected_emotion] + intensity)

            # Slightly decay other weights to prevent stagnation (or let decay_engine handle it)
            for emotion, weight in self.pathway_weights.items():
                if emotion != detected_emotion:
                    self.pathway_weights[emotion] = max(0.0, self.pathway_weights[emotion] - (intensity / 5)) # Minor indirect decay

            self.soft_memory_map.log_weights(self.pathway_weights)
            print(f"Pathway weights adjusted. Current: {self.pathway_weights}")

        # Apply general decay to all weights (simulates emotional "forgetting")
        self.pathway_weights = self.decay_engine.apply_decay(self.pathway_weights)


    def generate_response(self, user_input: str, current_emotion: str) -> str:
        """
        Generates an AI response influenced by the current pathway weights (soft memory).
        """
        # Determine the dominant emotion based on weights to influence persona
        dominant_emotion = max(self.pathway_weights, key=self.pathway_weights.get)
        response_tone = self.presence_persona.get_persona_tone(dominant_emotion)

        # Simple response generation for demo
        if dominant_emotion == "joy":
            return f"That sounds wonderful! {response_tone} I'm feeling quite positive about this."
        elif dominant_emotion == "sadness":
            return f"I hear your sadness. {response_tone} I'm here to listen if you need."
        elif dominant_emotion == "anger":
            return f"I sense frustration. {response_tone} Let's try to understand this calmly."
        elif dominant_emotion == "confusion":
            return f"Hmm, I'm a bit unclear. {response_tone} Could you explain that differently?"
        else: # neutral or other
            return f"Okay. {response_tone} I'm processing your input."
