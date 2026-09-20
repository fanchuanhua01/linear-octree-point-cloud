import numpy as np


def voxel_to_path(voxel, depth: int) -> tuple[int, ...]:
    ix, iy, iz = map(int, voxel)
    path = []

    for level in range(depth):
        shift = depth - level - 1
        x_bit = (ix >> shift) & 1
        y_bit = (iy >> shift) & 1
        z_bit = (iz >> shift) & 1
        path.append(4 * x_bit + 2 * y_bit + z_bit)

    return tuple(path)


def path_to_voxel(path) -> tuple[int, int, int]:
    ix = iy = iz = 0

    for octant in path:
        if not 0 <= octant <= 7:
            raise ValueError(f"非法八叉树节点编号：{octant}")

        ix = (ix << 1) | ((octant >> 2) & 1)
        iy = (iy << 1) | ((octant >> 1) & 1)
        iz = (iz << 1) | (octant & 1)

    return ix, iy, iz


def encode_voxels(voxels: np.ndarray, depth: int):
    return [voxel_to_path(voxel, depth) for voxel in voxels]


def decode_paths(paths) -> np.ndarray:
    if not paths:
        return np.empty((0, 3), dtype=np.int64)

    return np.asarray([path_to_voxel(path) for path in paths], dtype=np.int64)
