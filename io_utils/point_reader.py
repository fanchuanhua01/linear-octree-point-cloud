from pathlib import Path
import numpy as np


def read_txt_point_cloud(file_path: str) -> np.ndarray:
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{path}")

    rows = []

    with path.open("r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.replace(",", " ").replace("\t", " ").split()
            if len(parts) < 3:
                continue

            try:
                rows.append((
                    float(parts[0]),
                    float(parts[1]),
                    float(parts[2]),
                ))
            except ValueError:
                continue

    if not rows:
        raise ValueError("没有读取到有效 XYZ 坐标。")

    return np.asarray(rows, dtype=np.float64)
