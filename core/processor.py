from time import perf_counter

from core.metrics import chamfer_distance, hausdorff_distance
from core.octree import encode_voxels
from core.path_codec import decompose_paths, restore_paths
from core.preprocessing import clean_points, compute_aabb, normalize_points
from core.reconstruction import reconstruct_points
from core.voxel import points_to_voxels, unique_voxels
from models.result import ProcessResult


class PointCloudProcessor:
    def __init__(self, points):
        self.points = clean_points(points)
        self.aabb = compute_aabb(self.points)
        self.normalized_points = normalize_points(self.points, self.aabb)

    def process(self, depth: int) -> ProcessResult:
        start = perf_counter()

        voxels = points_to_voxels(self.normalized_points, depth)
        occupied_voxels = unique_voxels(voxels)

        full_paths = encode_voxels(occupied_voxels, depth)
        records = decompose_paths(full_paths, depth)
        restored_paths = restore_paths(records)

        if set(full_paths) != set(restored_paths):
            raise RuntimeError("路径分解与恢复结果不一致。")

        reconstructed = reconstruct_points(
            restored_paths,
            depth,
            self.aabb,
        )

        path_count = len(records)
        voxel_count = len(occupied_voxels)

        if path_count == 0:
            raise RuntimeError("当前深度下没有有效路径。")

        average = voxel_count / path_count

        if not 1.0 <= average <= 8.0:
            raise RuntimeError("每条路径平均携带体素数超出有效范围。")

        if len(reconstructed) != voxel_count:
            raise RuntimeError("重构点数与占用体素数不一致。")

        processing_time = perf_counter() - start

        cd = chamfer_distance(self.points, reconstructed)
        hd = hausdorff_distance(self.points, reconstructed)

        return ProcessResult(
            depth=depth,
            original_points=self.points,
            aabb=self.aabb,
            occupied_voxels=occupied_voxels,
            path_records=records,
            reconstructed_points=reconstructed,
            original_point_count=len(self.points),
            path_count=path_count,
            occupied_voxel_count=voxel_count,
            average_voxels_per_path=average,
            processing_time=processing_time,
            chamfer_distance=cd,
            hausdorff_distance=hd,
        )
