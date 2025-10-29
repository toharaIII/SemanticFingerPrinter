from fastapi import FastAPI, UploadFile, File, Form
from backend.orchestrator import call_orchestrator
from backend.embeddings import embed_texts
from backend.analysis import compute_centroid, find_closest_to_centroid, compute_variance
from typing import Optional, Union
import numpy as np

app = FastAPI(title="Semantic FingerPrinter API", version = "0.1")

@app.post("/analyze_prompt")
async def analyze_prompt(prompt: str = Form(...), mode: str = Form(...), n: int = Form(10), document: Optional[Union[UploadFile, str]] = File(None)):
    """
    Runs N orchestrator calls using the same prompt + optional document,
    embeds the results, finds the centroid, and returns the average output.
    """
    doc_content = None
    if document is not None:
        if isinstance(document, UploadFile):
            doc_content = await document.read()

    output = [call_orchestrator(prompt, mode, doc_content) for _ in range(n)]
    embeddings = embed_texts(output)
    embeddings = np.array(embeddings)

    centroid = compute_centroid(embeddings)
    variance = compute_variance(embeddings, centroid)
    avg_vec =  find_closest_to_centroid(embeddings, centroid)
    avg_output = output[avg_vec]

    result = {
        "average_output": avg_output,
        "outputs": [{"id": i, "text": t} for i, t in enumerate(output)],
        "embeddings_2d": embeddings.tolist(),
        "variance": variance
    }

    return result