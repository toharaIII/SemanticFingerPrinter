import numpy as np
from sklearn.metrics.pairwise import cosine_distances, cosine_similarity

def compute_centroid(embeddings: np.array) -> np.ndarray:
    return np.mean(embeddings, axis=0)

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