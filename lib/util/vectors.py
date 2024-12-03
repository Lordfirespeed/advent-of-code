from typing import Literal

import numpy as np


type Position = np.ndarray[tuple[Literal[2]], np.dtype[object]]


def pos(x: int, y: int) -> Position:
    return np.array([x, y], dtype=object)
