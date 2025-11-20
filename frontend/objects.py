from typing import Optional, Union
from pydantic import BaseModel
from fastapi import UploadFile

class AnalyzePromptRequest(BaseModel):
    userPrompt: str
    systemPrompt: str
    plan: Optional[str] = None
    n: int = 10
    #FOR FRONTEND IM NOT SURE THAT THIS IS THE CORRECT
    #DATATYPE FOR THE DOCUMENT, NEED TO LOOK INTO
    #WHAT STREAMLIT USES TO COLLECT DOCS
    document: Optional[UploadFile] = None
    temperature: Optional[float] = None
    topP: Optional[float] = None
    topK: Optional[int] = None
    maxTokens: Optional[int] = None
    stopSequences: Optional[Union[str,list[str]]] = None
    mcpServer: Optional[str] = None