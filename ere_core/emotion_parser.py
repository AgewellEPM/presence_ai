# presence_ai/ere_core/emotion_parser.py

def detect_emotion(text: str) -> str:
    """Very basic emotion detection stub."""
    text = text.lower()
    if any(word in text for word in ["happy", "joy", "excited", "love"]):
        return "joy"
    elif any(word in text for word in ["angry", "mad", "hate", "furious"]):
        return "rage"
    elif any(word in text for word in ["calm", "peaceful", "relaxed"]):
        return "calm"
    elif any(word in text for word in ["sacred", "spiritual", "holy"]):
        return "sacred"
    return "neutral"
