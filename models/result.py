from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class AABB:
    minimum: np.ndarray
    maximum: np.ndarray

    @property
    def size(self) -> np.ndarray:
        return self.maximum - self.minimum


@dataclass(frozen=True)
class PathRecord:
    prefix: tuple[int, ...]
    occupancy: tuple[int, ...]
    depth: int

    @property
    def occupancy_string(self) -> str:
        return "".join(str(v) for v in self.occupancy)

    @property
    def occupied_count(self) -> int:
        return sum(self.occupancy)


@dataclass
class ProcessResult:
    depth: int
    original_points: np.ndarray
    aabb: AABB
    occupied_voxels: np.ndarray
    path_records: list[PathRecord]
    reconstructed_points: np.ndarray
    original_point_count: int
    path_count: int
    occupied_voxel_count: int
    average_voxels_per_path: float
    processing_time: float
    chamfer_distance: float
    hausdorff_distance: float
