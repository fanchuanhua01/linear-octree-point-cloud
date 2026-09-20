import numpy as np


def points_to_voxels(points: np.ndarray, depth: int) -> np.ndarray:
    if depth < 1:
        raise ValueError("八叉树深度必须大于等于1。")

    resolution = 2 ** depth
    voxels = np.floor(points * resolution).astype(np.int64)
    return np.clip(voxels, 0, resolution - 1)


def unique_voxels(voxels: np.ndarray) -> np.ndarray:
    return np.unique(voxels, axis=0)


def voxel_centers(voxels: np.ndarray, depth: int) -> np.ndarray:
    resolution = 2 ** depth
    return (voxels.astype(np.float64) + 0.5) / resolution
