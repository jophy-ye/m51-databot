"""
common.py contains helper functions that could be used throughout m51 databot but don't deserve a separate file.
"""

import os


def get_ext(filename: str) -> str:
    return os.path.splitext(filename)[1]
