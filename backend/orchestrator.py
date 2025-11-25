import requests
from backend.objects import AnalyzePromptRequest

def call_orchestrator(request: AnalyzePromptRequest) -> str:
    
    orchURL = "orchestrator.com/replaceWithYourURL"

    payload = {
        "userPrompt": request.userPrompt,
        "systemPrompt": request.systemPrompt,
        "plan": request.plan,
        "temperature": request.temperature,
        "topP": request.topP,
        "topK": request.topK,
        "maxTokens": request.maxTokens,
        "stopSequences": request.stopSequences,
        "mcpServer": request.mcpServer
    }

    payload = {k: v for k, v in payload.items() if v is not None}
    
    try:
        if request.document:
            files = {"document": (request.document.filename, request.document.file, request.document.content_type)}
            response = requests.post(orchURL, data=payload, files=files)
        else:
            response = requests.post(orchURL, json=payload)

        response.raise_for_status
        return response.text.strip()
    
    except requests.exceptions as e:
        return {"success": False, "error": str(e), "status_code": e.response.status_code}