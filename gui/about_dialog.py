from PySide6.QtWidgets import QMessageBox
from config import SOFTWARE_NAME, VERSION


def show_about(parent):
    QMessageBox.information(
        parent,
        "关于软件",
        (
            f"{SOFTWARE_NAME}\n"
            f"版本：{VERSION}\n\n"
            "主要功能：点云读取、线性八叉树编码、路径分解、"
            "点云重构、重构质量分析、三维可视化和结果导出。"
        ),
    )


def show_help(parent):
    QMessageBox.information(
        parent,
        "使用说明",
        (
            "1. 点击“选择文件”加载 TXT 点云。\n"
            "2. 勾选需要计算的八叉树深度。\n"
            "3. 点击“开始分解与重构”。\n"
            "4. 在结果表中查看 D、N、Np、No、No/Np、Time、CD、HD。\n"
            "5. 使用 Open3D 显示原始点云、重构点云或对比结果。\n"
            "6. 点击“导出全部结果”保存 CSV、路径数据和重构点云。"
        ),
    )
