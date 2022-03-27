"""
Blog.py handles everything related to m51's live blog. It renders the HTML page with django and place it at the
appropriate folder. Class Blog and gen_blog() are provided to achieve this task.
"""

import os
import hashlib
import logging
from functools import lru_cache
from typing import List, Optional

from django.template import loader, Template

import settings
from utils.common import *


# type of post to bootstrap color code
COLOR_MAPPING = {
    '小道消息': 'warning',
    '決賽名單': 'success',
    '決賽成績': 'success',
    '複賽名單': 'primary',
    '複賽成績': 'primary',
    '初賽成績': 'secondary',
}
IMG_MAPPING = {
    '小道消息': '/imgs/jumping.png',
    '決賽名單': '/imgs/final.jpg',
    '決賽成績': '/imgs/final.jpg',
    '複賽名單': '/imgs/semi.jpg',
    '複賽成績': '/imgs/semi.jpg',
    '初賽成績': '/imgs/qual.jpg',
}


@lru_cache(maxsize=1)
def _table_template() -> Template:
    return loader.get_template('table.html')


@lru_cache(maxsize=1)
def _article_template() -> Template:
    return loader.get_template('article.html')


@lru_cache(maxsize=1)
def _blog_template() -> Template:
    return loader.get_template('live_blog.html')


# A class that generates a single article for the live blog
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

    def set_table(self, data: List[List[str]], rec: List[str]) -> None:
        self.escape = True
        # TODO: add support for 名單
        rows, cols = len(data), len(data[0])
        for r in range(rows):
            for c in range(cols):
                data[r][c] = str(data[r][c]).strip('"')  # these quotations appear everywhere in our csv files
            data[r].insert(0, str(r + 1))
            data[r][-1] += rec[r].strip('"')
        self.content = _table_template().render({'results': data})

    def compile(self, filename: Optional[str] = None):
        if not self.content:
            logging.error('compile() of Blog is called without having set its content')
            return
        if not filename:
            filename = f'{self.title}.html'
        # a (nearly) unique "id" of the article
        res = _article_template().render({
            'title': self.title,
            'label': self.label,
            'color_label': COLOR_MAPPING[self.label],
            'content': self.content,
            'img_path': IMG_MAPPING[self.label],
            'article_hash': hashlib.sha224(self.content.encode()).hexdigest()[:18],
        })
        with open(os.path.join(settings.HTML_DIR, filename), 'w', encoding='utf-8') as file:
            file.write(res)


# gen_blog() is used to gather all generated articles under html/ and put it into a single file
def gen_blog() -> None:
    article_list = os.listdir(settings.HTML_DIR)
    article_list.sort(key=lambda x: os.path.getmtime(os.path.join(settings.HTML_DIR, x)), reverse=True)

    articles = []
    for name in article_list:
        if not get_ext(name):     # escape dot files
            continue
        with open(os.path.join(settings.HTML_DIR, name), 'r', encoding='utf-8') as file:
            articles.append(file.read())
    res = _blog_template().render({'articles': articles})
    with open(settings.FINAL_BLOG, 'w', encoding='utf-8') as file:
        file.write(res)
