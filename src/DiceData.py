"""
# @ Author: FlowDND
# @ Create Time: 2025-08-01 20:53:34
# @ Description: FDRoller is a dice roller for TRPG.
"""

import numpy as np

PHI: float = (1 + np.sqrt(5)) / 2

DICE_NUMBER: dict[str, int] = {
    "d4": 4,
    "d6": 6,
    "d8": 8,
    "d10": 10,
    "d12": 12,
    "d20": 20,
}

DICE_VERTICES: dict[str, np.ndarray] = {
    "d4": np.array([[1, 1, 1], [1, -1, -1], [-1, 1, -1], [-1, -1, 1]]) * 1.5,
    "d6": np.array(
        [
            [1, 0, 0],
            [np.cos(2 * np.pi / 3), np.sin(2 * np.pi / 3), 0],
            [np.cos(4 * np.pi / 3), np.sin(4 * np.pi / 3), 0],
            [0, 0, 1],
            [0, 0, -1],
        ]
    ),
    "d8": np.array(
        [[1, 0, 0], [-1, 0, 0], [0, 1, 0], [0, -1, 0], [0, 0, 1], [0, 0, -1]]
    ),
    "d10": np.array(
        [
            [0, 0, 1.0],  # 顶点
            [0, 0, -1.0],  # 底点
            [1, 0, 0],
            [0.309, 0.951, 0],
            [-0.809, 0.588, 0],
            [-0.809, -0.588, 0],
            [0.309, -0.951, 0],
        ]
    ),
    "d12": np.array(
        [
            [1, 0, 0],
            [np.cos(np.pi / 3), np.sin(np.pi / 3), 0],
            [np.cos(2 * np.pi / 3), np.sin(2 * np.pi / 3), 0],
            [-1, 0, 0],
            [np.cos(4 * np.pi / 3), np.sin(4 * np.pi / 3), 0],
            [np.cos(5 * np.pi / 3), np.sin(5 * np.pi / 3), 0],
            [0, 0, 1.0],
            [0, 0, -1.0],
        ]
    ),
    "d20": np.array(
        [
            [-1, PHI, 0],
            [1, PHI, 0],
            [-1, -PHI, 0],
            [1, -PHI, 0],
            [0, -1, PHI],
            [0, 1, PHI],
            [0, -1, -PHI],
            [0, 1, -PHI],
            [PHI, 0, -1],
            [PHI, 0, 1],
            [-PHI, 0, -1],
            [-PHI, 0, 1],
        ]
    )
    / np.sqrt(1 + PHI**2),
}

DICE_FACES: dict[str, np.ndarray] = {
    "d4": np.array([[0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 3, 2]]),
    "d6": np.array([[0, 1, 3], [1, 2, 3], [2, 0, 3], [4, 1, 0], [4, 2, 1], [4, 0, 2]]),
    "d8": np.array(
        [
            [0, 2, 4],
            [0, 4, 3],
            [0, 3, 5],
            [0, 5, 2],
            [1, 4, 2],
            [1, 3, 4],
            [1, 5, 3],
            [1, 2, 5],
        ]
    ),
    "d10": np.array(
        [
            [0, 2, 3],
            [0, 3, 4],
            [0, 4, 5],
            [0, 5, 6],
            [0, 6, 2],
            [1, 3, 2],
            [1, 4, 3],
            [1, 5, 4],
            [1, 6, 5],
            [1, 2, 6],
        ]
    ),
    "d12": np.array(
        [
            [6, 1, 0],
            [6, 2, 1],
            [6, 3, 2],
            [6, 4, 3],
            [6, 5, 4],
            [6, 1, 5],
            [7, 0, 1],
            [7, 1, 2],
            [7, 2, 3],
            [7, 3, 4],
            [7, 4, 5],
            [7, 5, 0],
        ]
    ),
    "d20": np.array(
        [
            [0, 11, 5],
            [0, 5, 1],
            [0, 1, 7],
            [0, 7, 10],
            [0, 10, 11],
            [1, 5, 9],
            [5, 11, 4],
            [11, 10, 2],
            [10, 7, 6],
            [7, 1, 8],
            [3, 9, 4],
            [3, 4, 2],
            [3, 2, 6],
            [3, 6, 8],
            [3, 8, 9],
            [4, 9, 5],
            [2, 4, 11],
            [6, 2, 10],
            [8, 6, 7],
            [9, 8, 1],
        ]
    ),
}

DICE_CENTERS: dict[str, np.ndarray] = {
    dice: np.mean(DICE_VERTICES[dice], axis=0) for dice in DICE_VERTICES
}

DICE_FACE_CENTERS: dict[str, np.ndarray] = {
    dice: np.array(
        [np.mean(DICE_VERTICES[dice][face, :], axis=0) for face in DICE_FACES[dice]]
    )
    for dice in DICE_FACES
}
