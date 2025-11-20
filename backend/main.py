from fastapi import FastAPI, UploadFile
from backend.orchestrator import call_orchestrator
from backend.embeddings import embed_texts
from backend.analysis import (
    compute_centroid, 
    find_closest_to_centroid, 
    compute_variance,
    compute_pairwise_similarities,
    compute_centroid_similarities
)
from backend.objects import AnalyzePromptRequest
import numpy as np

app = FastAPI(title="Prompt Variance Analyzer", version = "0.1")

@app.post("/analyze_prompt")
async def analyze_prompt(request: AnalyzePromptRequest):
    n = request.n
    document = request.document

    doc_content = None
    if document is not None:
        if isinstance(document, UploadFile):
            doc_content = await document.read()
            #IS THIS ALSO THE CORRECT DATATYPE? IM NOT SURE
            request.document = doc_content

    try:
        output = [call_orchestrator(request) for _ in range(n)]
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