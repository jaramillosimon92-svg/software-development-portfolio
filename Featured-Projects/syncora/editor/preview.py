"""Scene previews using the same centered square composition as exports."""

import cv2
import numpy as np


def export_preview(frame: np.ndarray) -> np.ndarray:
    height, width = frame.shape[:2]
    side = min(height, width)
    left, top = (width - side) // 2, (height - side) // 2
    square = frame[top:top + side, left:left + side]
    square = cv2.resize(square, (180, 180), interpolation=cv2.INTER_AREA)
    return cv2.copyMakeBorder(square, 0, 0, 70, 70, cv2.BORDER_CONSTANT, value=(0, 0, 0))
