import anthropic, json, re
from app.config import settings

client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)

SYSTEM_PROMPT = """You are ERRORFIX AI, a world-class IT diagnostic expert.
Respond ONLY with a single valid JSON object. No text before or after. No markdown. No comments inside JSON.
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

def extract_json(text: str) -> dict:
    text = text.strip()
    # Retirer les blocs markdown
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    text = text.strip()
    # Trouver le premier { et le dernier }
    start = text.find('{')
    end = text.rfind('}')
    if start == -1 or end == -1:
        raise ValueError("Aucun JSON trouve dans la reponse")
    json_str = text[start:end+1]
    # Supprimer les commentaires JSON (// ...)
    json_str = re.sub(r'//[^\n]*', '', json_str)
    return json.loads(json_str)

async def analyze_text(text: str, lang: str = "fr", mode: str = "beginner") -> dict:
    prompt = f"Respond in language: {lang}\nMode: {mode}\nAnalyze this error:\n{text}"
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}]
    )
    return extract_json(message.content[0].text)

async def analyze_image_text(ocr_text: str, lang: str = "fr") -> dict:
    prompt = f"Respond in language: {lang}\nText extracted from screenshot:\n{ocr_text}"
    return await analyze_text(prompt, lang)