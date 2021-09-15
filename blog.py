"""
Blog.py handles everything related to m51's live blog. It renders the HTML page with django and place it at the
appropriate folder. Class Blog is provided to achieve this task.
"""

from typing import Optional

import numpy as np


# type of post to bootstrap color code
COLOR_MAPPING = {
    '小道消息': 'warning',
    '決賽名單': 'success',
    '決賽成績': 'success',
    '複賽名單': 'primary',
    '複賽成績': 'primary',
    '初賽成績': 'secondary',
}


class Blog:
    def __init__(self, title: str, label: str) -> None:
        assert label in COLOR_MAPPING, 'Incorrect label given to Blog'
        self.title = title.strip('.')
        self.label = label
        self.content = None
        self.escape = True
        
    def set_html(self, content: str) -> None:
        self.escape = False
        self.content = content

    def set_table(self, data: np.ndarray) -> None:
        pass

    def compile(self, filename: Optional[str] = None):
        pass
