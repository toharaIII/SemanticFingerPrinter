from fastapi import FastAPI, UploadFile, File, Form
from backend.orchestrator import call_orchestrator
from backend.embeddings import embed_texts
from backend.analysis import (
    compute_centroid, 
    find_closest_to_centroid, 
    compute_variance,
    compute_pairwise_similarities,
    compute_centroid_similarities
)
from typing import Optional, Union
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="Semantic FingerPrinter API", version = "0.1")

class AnalyzePromptRequest(BaseModel):
    userPrompt: str
    systemPrompt: str
    plan: Optional[str] = None
    n: int = 10
    document: Optional[UploadFile] = None
    temperature: Optional[float] = None
    topP: Optional[float] = None
    topK: Optional[int] = None
    maxTokens: Optional[int] = None
    stopSequences: Optional[Union[str,list[str]]] = None
    mcpServer: Optional[str] = None


@app.post("/analyze_prompt")
async def analyze_prompt(request: AnalyzePromptRequest):
    userPrompt = request.userPrompt
    systemPrompt = request.systemPrompt
    plan = request.plan
    n = request.n
    document = request.document
    temp = request.temperature
    topP = request.topP
    topK = request.topK
    maxTokens = request.maxTokens
    stopSequences = request.stopSequences
    mcp = request.mcpServer

    doc_content = None
    if document is not None:
        if isinstance(document, UploadFile):
            doc_content = await document.read()

    try:
        output = [call_orchestrator(userPrompt,systemPrompt,plan,doc_content,temp,topP,topK,maxTokens,stopSequences,mcp) for _ in range(n)]
    except Exception as e:
        return {"success": False, "error": str(e)}
    
    embeddings = embed_texts(output)
    embeddings = np.array(embeddings)

    similarities = compute_pairwise_similarities(embeddings)
    centroid = compute_centroid(embeddings)
    centroid_similarities = compute_centroid_similarities(embeddings, centroid)
    variance = compute_variance(embeddings, centroid)
    avg_vec =  find_closest_to_centroid(embeddings, centroid)
    avg_output = output[avg_vec]

    result = {
        "average_output": avg_output,
        "outputs": [{"id": i, "text": t} for i, t in enumerate(output)],
        "pairwise_similarities": similarities,
        "centroid_similarities": centroid_similarities,
        "variance": variance
    }

    return result