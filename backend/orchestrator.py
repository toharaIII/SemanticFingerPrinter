import requests
from fastapi import UploadFile

def call_orchestrator(userPrompt: str, systemPrompt: str, plan: str = None,
                      n: int = 10, document: UploadFile = None, temperature: float = None,
                      topP: float = None, topK: int = None, maxTokens: int = None,
                      stopSequences: str | list[str] = None, mcpServer: str = None) -> str:
    
    orchURL = "orchestrator.com/replaceWithYourURL"

    payload = {
        "userPrompt": userPrompt,
        "systemPrompt": systemPrompt,
        "plan": plan,
        "temperature": temperature,
        "topP": topP,
        "topK": topK,
        "maxTokens": maxTokens,
        "stopSequences": stopSequences,
        "mcpServer": mcpServer
    }

    payload = {k: v for k, v in payload.items() if v is not None}
    
    try:
        if document:
            files = {"document": (document.filename, document.file, document.content_type)}
            response = requests.post(orchURL, data=payload, files=files)
        else:
            response = requests.post(orchURL, json=payload)

        response.raise_for_status
        return response.text.strip()
    
    except requests.exceptions as e:
        return {"success": False, "error": str(e), "status_code": e.response.status_code}