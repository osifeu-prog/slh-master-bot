from deep_translator import GoogleTranslator

def to_english(text: str) -> str:
    if not text or len(text.strip()) < 2:
        return text
    try:
        return GoogleTranslator(source='auto', target='en').translate(text[:500]) or text
    except:
        return text

def from_english(text: str, target='iw') -> str:
    if not text or target == 'en':
        return text
    try:
        return GoogleTranslator(source='en', target=target).translate(text[:500]) or text
    except:
        return text
