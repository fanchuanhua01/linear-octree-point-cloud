from pathlib import Path
from datetime import datetime


class AppLogger:
    def __init__(self, log_dir):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        date_name = datetime.now().strftime("%Y%m%d")
        self.log_file = self.log_dir / f"software_{date_name}.log"

    def write(self, message: str):
        now = datetime.now().strftime("%H:%M:%S")
        line = f"[{now}] {message}"

        with self.log_file.open("a", encoding="utf-8") as file:
            file.write(line + "\n")

        return line
