from typing import Optional, Union
from pydantic import BaseModel

class AnalyzePromptRequest(BaseModel):
    userPrompt: str
    systemPrompt: str
    plan: Optional[str] = None
    n: int = 10
    document: Optional[bytes] = None
    temperature: Optional[float] = None
    topP: Optional[float] = None
    topK: Optional[int] = None
    maxTokens: Optional[int] = None
    stopSequences: Optional[Union[str,list[str]]] = None
    mcpServer: Optional[str] = None