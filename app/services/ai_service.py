import anthropic, json, re
from app.config import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are ERRORFIX AI, a world-class IT diagnostic expert.
Respond ONLY with a single valid JSON object. No text before or after. No markdown. No comments inside JSON. No control characters.
Schema:
{
  "code": "string or null",
  "title": "string",
  "category": "windows|linux|macos|android|ios|docker|sql|python|javascript|network|cloud|hardware|other",
  "detected_system": "string",
  "confidence": 0.85,
  "severity": "low|medium|high|critical",
  "causes": [{"description": "string", "probability": 0.7}],
  "impact": "string",
  "procedure_quick": [{"step": 1, "instruction": "string"}],
  "procedure_advanced": [{"step": 1, "instruction": "string", "command": "string"}],
  "commands": [{"os": "windows", "command": "string", "desc": "string"}],
  "prevention": "string"
}"""

def clean_json(text: str) -> dict:
    text = text.strip()
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    text = text.strip()
    start = text.find('{')
    end = text.rfind('}')
    if start == -1 or end == -1:
        raise ValueError("No JSON found")
    text = text[start:end+1]
    text = re.sub(r'//[^\n]*', '', text)
    text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
    return json.loads(text)

async def analyze_text(text: str, lang: str = "fr", mode: str = "beginner") -> dict:
    prompt = f"Respond in language: {lang}\nMode: {mode}\nAnalyze this error:\n{text}"
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return clean_json(message.content[0].text)

async def analyze_image_text(ocr_text: str, lang: str = "fr") -> dict:
    prompt = f"Respond in language: {lang}\nText extracted from screenshot:\n{ocr_text}"
    return await analyze_text(prompt, lang)