import numpy as np
from backend.analysis import (
    compute_centroid,
    compute_variance,
    compute_mean_distance
)

#run tests in this folder in command prompt via: python -m pytest -v

def generate_mock_embeddings(n=5, dim=4, seed=42):
    np.random.seed(seed)
    return np.random.rand(n, dim)


def test_compute_centroid():
    embeddings = generate_mock_embeddings()
    centroid = compute_centroid(embeddings)
    
    assert centroid.shape == (4,)
    same_vectors = np.ones((5, 4))
    centroid_same = compute_centroid(same_vectors)
    np.testing.assert_array_almost_equal(centroid_same, np.ones(4))


def test_compute_variance():
    embeddings = generate_mock_embeddings()
    centroid = compute_centroid(embeddings)
    var = compute_variance(embeddings, centroid)
    
    assert isinstance(var, float)
    assert var >= 0.0

    same_vectors = np.ones((5, 4))
    var_same = compute_variance(same_vectors, compute_centroid(same_vectors))
    assert np.isclose(var_same, 0.0)


def test_compute_mean_distance():
    embeddings = generate_mock_embeddings()
    centroid = compute_centroid(embeddings)
    mean_dist = compute_mean_distance(embeddings, centroid)
    
    assert isinstance(mean_dist, float)
    assert mean_dist >= 0.0

    same_vectors = np.ones((5, 4))
    mean_dist_same = compute_mean_distance(same_vectors, compute_centroid(same_vectors))
    assert np.isclose(mean_dist_same, 0.0)


def test_variance_zero():
    embeddings = np.array([[1, 2, 3],
                           [1, 2, 3],
                           [1, 2, 3]])
    centroid = np.array([1, 2, 3])
    result = compute_variance(embeddings, centroid)
    assert result == 0.0


def test_variance_known_case():
    embeddings = np.array([
        [1, 0],  # 1 unit right
        [-1, 0], # 1 unit left
        [0, 1],  # 1 unit up
        [0, -1]  # 1 unit down
    ])
    centroid = np.array([0, 0])
    result = compute_variance(embeddings, centroid)
    assert np.isclose(result, 1.0)


def test_variance_random_shape():
    rng = np.random.default_rng(seed=42)
    embeddings = rng.random((10, 5))
    centroid = embeddings.mean(axis=0)
    result = compute_variance(embeddings, centroid)
    assert isinstance(result, float)
    assert result >= 0