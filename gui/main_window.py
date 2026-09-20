from pathlib import Path

from PySide6.QtCore import Qt, QThread
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QGroupBox, QLabel, QLineEdit, QPushButton, QFileDialog,
    QMessageBox, QCheckBox, QComboBox, QTableWidget,
    QTableWidgetItem, QTextEdit, QHeaderView, QStatusBar,
)

from config import (
    SOFTWARE_NAME, VERSION, SUPPORTED_DEPTHS, DEFAULT_DEPTHS,
    OUTPUT_DIR, LOG_DIR, WINDOW_WIDTH, WINDOW_HEIGHT,
)
from gui.about_dialog import show_about, show_help
from gui.worker import ProcessWorker
from io_utils.point_reader import read_txt_point_cloud
from io_utils.result_writer import export_all
from utils.logger import AppLogger
from visualization.open3d_viewer import (
    show_original, show_reconstructed, show_comparison,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.file_path = None
        self.points = None
        self.results = {}
        self.thread = None
        self.worker = None
        self.logger = AppLogger(LOG_DIR)

        self.setWindowTitle(f"{SOFTWARE_NAME} {VERSION}")
        self.resize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self._build_menu()
        self._build_ui()

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

        self._log("软件启动完成")

    def _build_menu(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("文件")
        open_action = file_menu.addAction("打开点云")
        open_action.triggered.connect(self.select_file)

        export_action = file_menu.addAction("导出全部结果")
        export_action.triggered.connect(self.export_results)

        file_menu.addSeparator()
        exit_action = file_menu.addAction("退出")
        exit_action.triggered.connect(self.close)

        view_menu = menu_bar.addMenu("视图")
        view_menu.addAction("显示原始点云").triggered.connect(
            self.show_original_cloud
        )
        view_menu.addAction("显示重构点云").triggered.connect(
            self.show_reconstructed_cloud
        )
        view_menu.addAction("原始/重构对比").triggered.connect(
            self.show_comparison_cloud
        )

        help_menu = menu_bar.addMenu("帮助")
        help_menu.addAction("使用说明").triggered.connect(
            lambda: show_help(self)
        )
        help_menu.addAction("关于软件").triggered.connect(
            lambda: show_about(self)
        )

    def _build_ui(self):
        central = QWidget()
        self.setCentralWidget(central)

        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(12, 12, 12, 12)
        main_layout.setSpacing(12)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        left_layout.setSpacing(10)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        right_layout.setSpacing(10)

        main_layout.addWidget(left, 0)
        main_layout.addWidget(right, 1)

        left_layout.addWidget(self._build_file_group())
        left_layout.addWidget(self._build_depth_group())
        left_layout.addWidget(self._build_action_group())
        left_layout.addStretch()

        right_layout.addWidget(self._build_info_group())
        right_layout.addWidget(self._build_result_group(), 1)
        right_layout.addWidget(self._build_log_group())

    def _build_file_group(self):
        group = QGroupBox("点云文件")
        layout = QVBoxLayout(group)

        self.file_edit = QLineEdit()
        self.file_edit.setReadOnly(True)

        button = QPushButton("选择文件")
        button.clicked.connect(self.select_file)

        layout.addWidget(self.file_edit)
        layout.addWidget(button)
        return group

    def _build_depth_group(self):
        group = QGroupBox("八叉树深度")
        layout = QGridLayout(group)
        self.depth_checks = {}

        for index, depth in enumerate(SUPPORTED_DEPTHS):
            checkbox = QCheckBox(f"D = {depth}")
            checkbox.setChecked(depth in DEFAULT_DEPTHS)
            self.depth_checks[depth] = checkbox
            layout.addWidget(checkbox, index // 2, index % 2)

        return group

    def _build_action_group(self):
        group = QGroupBox("操作")
        layout = QVBoxLayout(group)

        self.process_button = QPushButton("开始分解与重构")
        self.process_button.clicked.connect(self.start_processing)

        self.depth_combo = QComboBox()
        self.depth_combo.setPlaceholderText("选择重构深度")

        original_button = QPushButton("显示原始点云")
        original_button.clicked.connect(self.show_original_cloud)

        reconstructed_button = QPushButton("显示重构点云")
        reconstructed_button.clicked.connect(self.show_reconstructed_cloud)

        compare_button = QPushButton("原始/重构对比")
        compare_button.clicked.connect(self.show_comparison_cloud)

        export_button = QPushButton("导出全部结果")
        export_button.clicked.connect(self.export_results)

        layout.addWidget(self.process_button)
        layout.addSpacing(6)
        layout.addWidget(original_button)
        layout.addWidget(self.depth_combo)
        layout.addWidget(reconstructed_button)
        layout.addWidget(compare_button)
        layout.addSpacing(6)
        layout.addWidget(export_button)

        return group

    def _build_info_group(self):
        group = QGroupBox("点云基本信息")
        layout = QGridLayout(group)

        self.info_labels = {
            "name": QLabel("-"),
            "count": QLabel("-"),
            "x": QLabel("-"),
            "y": QLabel("-"),
            "z": QLabel("-"),
        }

        labels = [
            ("文件名称：", "name"),
            ("原始点数：", "count"),
            ("X 范围：", "x"),
            ("Y 范围：", "y"),
            ("Z 范围：", "z"),
        ]

        for row, (title, key) in enumerate(labels):
            layout.addWidget(QLabel(title), row, 0)
            layout.addWidget(self.info_labels[key], row, 1)

        return group

    def _build_result_group(self):
        group = QGroupBox("处理结果")
        layout = QVBoxLayout(group)

        headers = ["D", "N", "Np", "No", "No/Np", "Time(s)", "CD", "HD"]

        self.result_table = QTableWidget(0, len(headers))
        self.result_table.setHorizontalHeaderLabels(headers)
        self.result_table.setEditTriggers(
            QTableWidget.EditTrigger.NoEditTriggers
        )
        self.result_table.setSelectionBehavior(
            QTableWidget.SelectionBehavior.SelectRows
        )
        self.result_table.verticalHeader().setVisible(False)
        self.result_table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Stretch
        )

        layout.addWidget(self.result_table)
        return group

    def _build_log_group(self):
        group = QGroupBox("运行日志")
        layout = QVBoxLayout(group)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumHeight(170)

        layout.addWidget(self.log_text)
        return group

    def _log(self, message):
        line = self.logger.write(message)
        self.log_text.append(line)
        self.status_bar.showMessage(message)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择点云文件",
            "",
            "TXT Point Cloud (*.txt);;All Files (*)",
        )

        if not file_path:
            return

        try:
            points = read_txt_point_cloud(file_path)

            self.file_path = file_path
            self.points = points
            self.results.clear()
            self.result_table.setRowCount(0)
            self.depth_combo.clear()
            self.file_edit.setText(file_path)

            self._update_point_info()
            self._log(
                f"已加载 {Path(file_path).name}，有效点数 {len(points)}"
            )

        except Exception as exc:
            QMessageBox.critical(self, "读取失败", str(exc))
            self._log(f"读取点云失败：{exc}")

    def _update_point_info(self):
        points = self.points

        self.info_labels["name"].setText(Path(self.file_path).name)
        self.info_labels["count"].setText(str(len(points)))
        self.info_labels["x"].setText(
            f"{points[:, 0].min():.6f} ~ {points[:, 0].max():.6f}"
        )
        self.info_labels["y"].setText(
            f"{points[:, 1].min():.6f} ~ {points[:, 1].max():.6f}"
        )
        self.info_labels["z"].setText(
            f"{points[:, 2].min():.6f} ~ {points[:, 2].max():.6f}"
        )

    def _selected_depths(self):
        return [
            depth
            for depth, checkbox in self.depth_checks.items()
            if checkbox.isChecked()
        ]

    def start_processing(self):
        if self.points is None:
            QMessageBox.warning(self, "提示", "请先选择点云文件。")
            return

        depths = self._selected_depths()
        if not depths:
            QMessageBox.warning(self, "提示", "请至少选择一个八叉树深度。")
            return

        self.results.clear()
        self.result_table.setRowCount(0)
        self.depth_combo.clear()
        self.process_button.setEnabled(False)

        self._log("开始处理，深度：" + ", ".join(map(str, depths)))

        self.thread = QThread()
        self.worker = ProcessWorker(self.points, depths)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self._log)
        self.worker.result_ready.connect(self._receive_result)
        self.worker.failed.connect(self._processing_failed)
        self.worker.finished.connect(self._processing_finished)

        self.worker.finished.connect(self.thread.quit)
        self.worker.failed.connect(self.thread.quit)

        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _receive_result(self, result):
        self.results[result.depth] = result
        self._append_result_row(result)

    def _append_result_row(self, result):
        row = self.result_table.rowCount()
        self.result_table.insertRow(row)

        values = [
            str(result.depth),
            str(result.original_point_count),
            str(result.path_count),
            str(result.occupied_voxel_count),
            f"{result.average_voxels_per_path:.4f}",
            f"{result.processing_time:.6f}",
            f"{result.chamfer_distance:.8g}",
            f"{result.hausdorff_distance:.8g}",
        ]

        for col, value in enumerate(values):
            item = QTableWidgetItem(value)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.result_table.setItem(row, col, item)

    def _processing_finished(self):
        self.process_button.setEnabled(True)
        self.depth_combo.clear()

        for depth in sorted(self.results):
            self.depth_combo.addItem(f"Depth {depth}", depth)

        self._log("全部处理完成")

    def _processing_failed(self, message):
        self.process_button.setEnabled(True)
        QMessageBox.critical(self, "处理失败", message)
        self._log(f"处理失败：{message}")

    def show_original_cloud(self):
        if self.points is None:
            QMessageBox.warning(self, "提示", "请先加载点云。")
            return

        self._log("打开原始点云窗口")
        show_original(self.points)

    def _current_result(self):
        depth = self.depth_combo.currentData()

        if depth is None or depth not in self.results:
            QMessageBox.warning(
                self,
                "提示",
                "请先完成处理并选择一个重构深度。",
            )
            return None

        return self.results[depth]

    def show_reconstructed_cloud(self):
        result = self._current_result()
        if result is None:
            return

        self._log(f"打开 D={result.depth} 重构点云窗口")
        show_reconstructed(
            result.reconstructed_points,
            result.depth,
        )

    def show_comparison_cloud(self):
        result = self._current_result()
        if result is None:
            return

        self._log(f"打开 D={result.depth} 对比窗口")
        show_comparison(
            result.original_points,
            result.reconstructed_points,
            result.depth,
        )

    def export_results(self):
        if not self.results:
            QMessageBox.warning(self, "提示", "当前没有可导出的处理结果。")
            return

        export_root = QFileDialog.getExistingDirectory(
            self,
            "选择结果保存目录",
            str(OUTPUT_DIR),
        )

        if not export_root:
            return

        try:
            results = [self.results[depth] for depth in sorted(self.results)]
            export_dir = export_all(results, export_root, self.file_path)

            self._log(f"结果已导出：{export_dir}")
            QMessageBox.information(
                self,
                "导出完成",
                f"结果已保存到：\n{export_dir}",
            )

        except Exception as exc:
            QMessageBox.critical(self, "导出失败", str(exc))
            self._log(f"导出失败：{exc}")
