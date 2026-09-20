import numpy as np
from models.result import AABB


def clean_points(points: np.ndarray) -> np.ndarray:
    points = np.asarray(points, dtype=np.float64)
    if points.ndim != 2 or points.shape[1] != 3:
        raise ValueError("点云数据必须为 Nx3 数组。")

    points = points[np.isfinite(points).all(axis=1)]
    if len(points) == 0:
        raise ValueError("点云中没有有效坐标。")
    return points


def compute_aabb(points: np.ndarray) -> AABB:
    return AABB(np.min(points, axis=0), np.max(points, axis=0))


def normalize_points(points: np.ndarray, aabb: AABB) -> np.ndarray:
    size = aabb.size
    normalized = np.empty_like(points, dtype=np.float64)

    for axis in range(3):
        if size[axis] == 0:
            normalized[:, axis] = 0.5
        else:
            normalized[:, axis] = (
                points[:, axis] - aabb.minimum[axis]
            ) / size[axis]

    return np.clip(normalized, 0.0, 1.0)


def denormalize_points(points: np.ndarray, aabb: AABB) -> np.ndarray:
    size = aabb.size
    restored = np.empty_like(points, dtype=np.float64)

    for axis in range(3):
        if size[axis] == 0:
            restored[:, axis] = aabb.minimum[axis]
        else:
            restored[:, axis] = aabb.minimum[axis] + points[:, axis] * size[axis]

    return restored
