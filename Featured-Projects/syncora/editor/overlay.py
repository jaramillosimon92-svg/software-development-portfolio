"""Detect the centered DREHTV bumper in scene previews."""

from functools import lru_cache
from pathlib import Path

import cv2
import numpy as np


@lru_cache(maxsize=1)
def _reference() -> np.ndarray:
    path = Path(__file__).parent / "assets" / "drehtv_logo_reference.png"
    reference = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if reference is None:
        raise RuntimeError(f"Overlay reference is missing: {path}")
    return reference


def centered_logo_score(square_preview: np.ndarray) -> float:
    """Match the known bumper near the middle of a 180x180 scene preview."""
    if square_preview.shape[:2] != (180, 180):
        raise ValueError("Expected a 180x180 square preview.")
    gray = cv2.cvtColor(square_preview, cv2.COLOR_BGR2GRAY)
    search = gray[55:120, 70:115]
    return float(cv2.matchTemplate(search, _reference(), cv2.TM_CCOEFF_NORMED).max())
