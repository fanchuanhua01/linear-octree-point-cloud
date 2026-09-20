from pathlib import Path

SOFTWARE_NAME = "三维点云线性八叉树分解与重构系统"
VERSION = "V1.0"

DEFAULT_DEPTHS = [4, 5, 6]
SUPPORTED_DEPTHS = list(range(2, 9))

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
LOG_DIR = BASE_DIR / "logs"

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 820
