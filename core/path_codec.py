from models.result import PathRecord


def decompose_paths(paths, depth: int):
    grouped = {}

    # 按 D-1 层父路径合并末级体素
    for path in paths:
        if len(path) != depth:
            raise ValueError("路径长度与八叉树深度不一致。")

        prefix = tuple(path[:-1])
        terminal = int(path[-1])

        if prefix not in grouped:
            grouped[prefix] = [0] * 8

        grouped[prefix][terminal] = 1

    records = [
        PathRecord(prefix, tuple(occupancy), depth)
        for prefix, occupancy in grouped.items()
    ]
    records.sort(key=lambda item: item.prefix)
    return records


def restore_paths(records):
    paths = []

    for record in records:
        for terminal, occupied in enumerate(record.occupancy):
            if occupied:
                paths.append(record.prefix + (terminal,))

    paths.sort()
    return paths
