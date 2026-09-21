# 三维点云线性八叉树分解与重构系统

**Linear Octree Point Cloud Decomposition and Reconstruction System**

## 项目简介

本项目基于 Python 开发，实现三维点云的读取、预处理、线性八叉树分解、路径编码、点云重构、精度评价和三维可视化等功能。

系统通过八叉树对三维空间进行层次划分，并将有效空间节点转换为路径编码，实现点云空间结构的紧凑表达；随后根据路径编码和体素信息完成点云重构，并使用 Chamfer Distance（CD）和 Hausdorff Distance（HD）对重构结果进行评价。

项目采用 PySide6 构建图形用户界面，并结合 Open3D 实现原始点云与重构点云的三维可视化。

## 主要功能

- 点云文件读取与数据预处理
- 三维空间归一化与体素划分
- 线性八叉树构建
- 八叉树路径编码与解析
- 点云重构
- Chamfer Distance（CD）计算
- Hausdorff Distance（HD）计算
- 原始点云与重构点云三维可视化
- 分解与重构结果导出
- PySide6 图形用户界面
- 系统运行日志记录

## 技术栈

- Python
- NumPy
- SciPy
- Open3D
- PySide6
- Visual Studio Code

## 项目结构

- `core`：八叉树构建、路径编码、重构和评价指标
- `gui`：PySide6 图形界面
- `io_utils`：点云读取与结果保存
- `models`：数据结构
- `visualization`：Open3D 可视化
- `utils`：日志等通用功能