import numpy as np
from core.octree import decode_paths
from core.preprocessing import denormalize_points
from core.voxel import voxel_centers


def reconstruct_points(paths, depth, aabb) -> np.ndarray:
    voxels = decode_paths(paths)
    if len(voxels) == 0:
        return np.empty((0, 3), dtype=np.float64)

    centers = voxel_centers(voxels, depth)
    return denormalize_points(centers, aabb)
