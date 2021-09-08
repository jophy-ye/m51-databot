"""
FSDiff.py contains the FSDiff class.

If a dir is given to FSDiff, it monitors the changes of files within the dir and returns a list of (filename, version)
tuples. (Version is a positive integer.) When an ext is given to file_change(), FSDiff only checks files with that
particular extension.
"""

import os
import json
import logging
import time
from math import inf
from typing import List

import settings


INTERNAL_DATA_FILE = os.path.join(settings.DATA_DIR, 'm51_data.json')


class FSDiff:
    def __init__(self, path: str, ext: str = '.') -> None:
        self.dir = path
        self.ext = ext

    def file_change(self) -> List[tuple]:
        with open(INTERNAL_DATA_FILE, 'r', encoding='utf-8') as _file:
            int_file = json.load(_file)             # old info loaded from data/m51_data.json
        data = int_file.setdefault('watched', {})   # "watched" contains all watched files by FSDiff

        diff_files = []
        for file in os.listdir(self.dir):
            if self.ext not in os.path.splitext(file)[1]:
                continue
            try:
                ts = os.path.getmtime(os.path.join(self.dir, file))
            except OSError:
                logging.error(f"path for {file} doesn't exist or is inaccessible", exc_info=True)
                continue

            data.setdefault(file, {'version': 0, 'timestamp': -inf})
            if data[file]['timestamp'] >= ts:
                continue
            data[file]['version'] += 1
            data[file]['timestamp'] = time.time()
            diff_files.append((file, data[file]['version']))

        with open(INTERNAL_DATA_FILE, 'w', encoding='utf-8') as _file:
            json.dump(int_file, _file)
        return diff_files
