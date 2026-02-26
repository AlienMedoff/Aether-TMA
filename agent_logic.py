import json

def safe_extract_json(text):
    try:
        start = text.find("{")
        end = text.rfind("}") + 1
        return json.loads(text[start:end])
    except:
        return {"thought": "Error parsing JSON", "action": {"type": "none"}}

def get_system_prompt():
    return """
    ROLE: Strategic Navigator for Telegram Mini Apps.
    FORMAT: Respond ONLY with JSON.
    SCHEMA: {"thought": "string", "action": {"type": "click|type|none", "target": "element_id"}}
    """
