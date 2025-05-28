# presence_ai/ere_core/reaction_mapper.py

import json
import os
from config.config import Config

class ReactionMapper:
    def __init__(self):
        self.config = Config()
        
        # Path to emotion_reactor.json, deriving it from the base project directory
        # This assumes emotion_reactor.json is consistently in virem_vault/
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.emotion_reactor_path = os.path.join(base_dir, "virem_vault", "emotion_reactor.json")
        
        self.reaction_map = self._load_reaction_map()
        print(f"ReactionMapper initialized. Loaded mappings from: {self.emotion_reactor_path}")

    def _load_reaction_map(self) -> dict:
        """Loads emotion reaction rules (emojis, conceptual sound/haptic) from emotion_reactor.json."""
        try:
            with open(self.emotion_reactor_path, 'r') as f:
                data = json.load(f)
                reaction_data = {}
                for emotion, rules in data.get("emotion_rules", {}).items():
                    emojis = rules.get("emojis", [])
                    # Take the first emoji as the primary visual reaction
                    visual_reaction = emojis[0] if emojis else ""
                    
                    reaction_data[emotion] = {
                        "visual": visual_reaction,
                        "sound": f"sound_{emotion}.wav",      # Conceptual sound file path
                        "haptic": f"haptic_pattern_{emotion}" # Conceptual haptic pattern ID
                    }
                return reaction_data
        except FileNotFoundError:
            print(f"Error: {self.emotion_reactor_path} not found. Using default internal reactions.")
            return self._get_default_reactions()
        except json.JSONDecodeError:
            print(f"Error: Could not decode JSON from {self.emotion_reactor_path}. Using default internal reactions.")
            return self._get_default_reactions()

    def _get_default_reactions(self) -> dict:
        """Provides fallback default reactions if loading fails."""
        return {
            "joy": {"visual": "😊", "sound": "", "haptic": ""},
            "rage": {"visual": "😡", "sound": "", "haptic": ""},
            "calm": {"visual": "😌", "sound": "", "haptic": ""},
            "sacred": {"visual": "✨", "sound": "", "haptic": ""},
            "neutral": {"visual": "😐", "sound": "", "haptic": ""},
            # Add any other emotions you might have, with default fallback reactions
        }

    def get_reaction(self, emotion: str) -> dict:
        """
        Returns a dictionary of reactions (visual, sound, haptic) for a given emotion.
        Returns a default reaction if the emotion is not mapped.
        """
        return self.reaction_map.get(emotion, {
            "visual": "❓", "sound": "", "haptic": "" # Default for unmapped emotions
        })
