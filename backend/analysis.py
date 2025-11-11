import numpy as np
from sklearn.metrics.pairwise import cosine_distances, cosine_similarity

def compute_pairwise_similarities(embeddings: np.array) -> list:
    embeddings_array = np.array(embeddings)
    similaries = cosine_similarity(embeddings_array)
    return similaries.tolist()

def compute_centroid(embeddings: np.array) -> np.ndarray:
    if embeddings.size == 0:
        raise ValueError("No embeddings provided — cannot compute centroid.")
    elif len(embeddings.shape) == 1:
        embeddings = np.expand_dims(embeddings, axis=0)
    return np.mean(embeddings, axis=0)

def compute_centroid_similarities(embeddings: np.ndarray, centroid: np.ndarray) -> list:
    centroid_reshaped = centroid.reshape(1, -1)
    similarities = cosine_similarity(embeddings, centroid_reshaped)
    return similarities.flatten().tolist()

def find_closest_to_centroid(embeddings: np.ndarray, centroid: np.ndarray) -> int:
    distances = cosine_distances(embeddings, [centroid]).flatten()
    return int(np.argmin(distances))

def compute_variance(embeddings: np.ndarray, centroid: np.ndarray) -> float:
    """
    this one for MVP
    """
    distances = np.linalg.norm(embeddings - centroid, axis=1)
    return float(np.mean(distances ** 2))

def compute_mean_distance(embeddings: np.ndarray, centroid: np.ndarray) -> float:
    distances = np.linalg.norm(embeddings - centroid, axis=1)
    return float(np.mean(distances))

def compute_cosine_variance(embeddings: np.ndarray, centroid: np.ndarray) -> float:
    similarities = cosine_similarity(embeddings, centroid.reshape(1, -1)).flatten
    return float(1 - np.mean(similarities))