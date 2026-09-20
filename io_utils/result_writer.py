from pathlib import Path
from datetime import datetime
import csv
import numpy as np


def create_export_dir(base_dir, source_file):
    base_dir = Path(base_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    source_name = Path(source_file).stem
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_dir = base_dir / f"{source_name}_{timestamp}"
    export_dir.mkdir(parents=True, exist_ok=True)

    return export_dir


def save_summary(results, export_dir):
    file_path = Path(export_dir) / "summary.csv"

    with file_path.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow([
            "Depth",
            "OriginalPoints_N",
            "PathCount_Np",
            "OccupiedVoxels_No",
            "Average_No_Np",
            "ProcessingTime_s",
            "ChamferDistance",
            "HausdorffDistance",
        ])

        for result in results:
            writer.writerow([
                result.depth,
                result.original_point_count,
                result.path_count,
                result.occupied_voxel_count,
                f"{result.average_voxels_per_path:.6f}",
                f"{result.processing_time:.6f}",
                f"{result.chamfer_distance:.12g}",
                f"{result.hausdorff_distance:.12g}",
            ])

    return file_path


def save_depth_result(result, export_dir):
    depth_dir = Path(export_dir) / f"depth_{result.depth}"
    depth_dir.mkdir(parents=True, exist_ok=True)

    path_file = depth_dir / "path_records.csv"
    with path_file.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.writer(file)
        writer.writerow(["PathID", "Prefix", "Occupancy", "OccupiedCount"])

        for index, record in enumerate(result.path_records, start=1):
            writer.writerow([
                index,
                "-".join(map(str, record.prefix)),
                record.occupancy_string,
                record.occupied_count,
            ])

    point_file = depth_dir / "reconstructed.xyz"
    np.savetxt(point_file, result.reconstructed_points, fmt="%.10f")

    return path_file, point_file


def export_all(results, base_dir, source_file):
    export_dir = create_export_dir(base_dir, source_file)
    save_summary(results, export_dir)

    for result in results:
        save_depth_result(result, export_dir)

    return export_dir
