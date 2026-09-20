import numpy as np
import open3d as o3d


def _make_cloud(points: np.ndarray):
    cloud = o3d.geometry.PointCloud()
    cloud.points = o3d.utility.Vector3dVector(points)
    return cloud


def show_original(points: np.ndarray):
    cloud = _make_cloud(points)
    o3d.visualization.draw_geometries(
        [cloud],
        window_name="Original Point Cloud",
    )


def show_reconstructed(points: np.ndarray, depth: int):
    cloud = _make_cloud(points)
    o3d.visualization.draw_geometries(
        [cloud],
        window_name=f"Reconstructed Point Cloud - Depth {depth}",
    )


def show_comparison(original: np.ndarray, reconstructed: np.ndarray, depth: int):
    original_cloud = _make_cloud(original)
    reconstructed_cloud = _make_cloud(reconstructed)

    original_cloud.paint_uniform_color([0.20, 0.60, 1.00])
    reconstructed_cloud.paint_uniform_color([1.00, 0.30, 0.20])

    o3d.visualization.draw_geometries(
        [original_cloud, reconstructed_cloud],
        window_name=f"Comparison - Depth {depth}",
    )
