"""
common.py contains helper functions that could be used throughout m51 databot but don't deserve a separate file.
"""

import os


FIELD_KEYWORDS = ('跳高', '跳遠', '三級跳遠', '推鉛球', '擲壘球')
NAN_KEYWORDS = ('"缺"', '"無成績"', '"3"')


def get_ext(filename: str) -> str:
    return os.path.splitext(filename)[1]


def is_field(comp: str) -> bool:
    for key in FIELD_KEYWORDS:
        if key in comp:
            return True
    return False
