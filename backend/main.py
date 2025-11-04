from fastapi import FastAPI, UploadFile, File, Form
from backend.orchestrator import call_orchestrator
from backend.embeddings import embed_texts
from backend.analysis import (
    compute_centroid, 
    find_closest_to_centroid, 
    compute_variance,
    compute_pairwise_similarities
)
from typing import Optional, Union
from pydantic import BaseModel
import numpy as np

app = FastAPI(title="Semantic FingerPrinter API", version = "0.1")

class AnalyzePromptRequest(BaseModel):
    prompt: str
    plan: Optional[str] = None
    n: int = 10
    document: Optional[str] = None

@app.post("/analyze_prompt")
async def analyze_prompt(request: AnalyzePromptRequest):
    prompt = request.prompt
    plan = request.plan
    n = request.n
    document = request.document

    doc_content = None
    if document is not None:
        if isinstance(document, UploadFile):
            doc_content = await document.read()

    output = [call_orchestrator(prompt, plan, doc_content) for _ in range(n)]
    embeddings = embed_texts(output)
    embeddings = np.array(embeddings)

    similarities = compute_pairwise_similarities(embeddings)
    centroid = compute_centroid(embeddings)
    variance = compute_variance(embeddings, centroid)
    avg_vec =  find_closest_to_centroid(embeddings, centroid)
    avg_output = output[avg_vec]

    result = {
        "average_output": avg_output,
        "outputs": [{"id": i, "text": t} for i, t in enumerate(output)],
        "pairwise_similarities": similarities,
        "variance": variance
    }

    return result