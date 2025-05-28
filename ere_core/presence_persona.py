# presence_ai/ere_core/presence_persona.py

class PresencePersona:
    def __init__(self):
        # Define base tones or phrases associated with dominant emotions
        self.persona_tones = {
            "joy": " (with a light and uplifting tone)",
            "rage": " (with a firm but calming tone)",
            "calm": " (with a serene and steady tone)",
            "sacred": " (with a reverent and profound tone)",
            "neutral": " (with a balanced and observant tone)"
        }
        print("PresencePersona initialized.")

    def get_persona_tone(self, dominant_emotion: str) -> str:
        """
        Returns a string snippet that can be appended to a response
        to give it a particular emotional 'tone' based on the
        AI's current dominant internal affective state.
        """
        return self.persona_tones.get(dominant_emotion, " (with an adaptive tone)")
