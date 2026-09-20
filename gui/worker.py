from PySide6.QtCore import QObject, Signal, Slot
from core.processor import PointCloudProcessor


class ProcessWorker(QObject):
    progress = Signal(str)
    result_ready = Signal(object)
    finished = Signal()
    failed = Signal(str)

    def __init__(self, points, depths):
        super().__init__()
        self.points = points
        self.depths = depths

    @Slot()
    def run(self):
        try:
            processor = PointCloudProcessor(self.points)

            for depth in self.depths:
                self.progress.emit(f"正在处理深度 D={depth} ...")
                result = processor.process(depth)
                self.result_ready.emit(result)
                self.progress.emit(f"深度 D={depth} 处理完成")

            self.finished.emit()

        except Exception as exc:
            self.failed.emit(str(exc))
