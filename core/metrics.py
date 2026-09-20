import numpy as np
from scipy.spatial import cKDTree


def chamfer_distance(points_a: np.ndarray, points_b: np.ndarray) -> float:
    tree_a = cKDTree(points_a)
    tree_b = cKDTree(points_b)

    dist_ab, _ = tree_b.query(points_a, k=1)
    dist_ba, _ = tree_a.query(points_b, k=1)

    return float(np.mean(dist_ab ** 2) + np.mean(dist_ba ** 2))


def hausdorff_distance(points_a: np.ndarray, points_b: np.ndarray) -> float:
    tree_a = cKDTree(points_a)
    tree_b = cKDTree(points_b)

    dist_ab, _ = tree_b.query(points_a, k=1)
    dist_ba, _ = tree_a.query(points_b, k=1)

    return float(max(np.max(dist_ab), np.max(dist_ba)))
