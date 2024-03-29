"""
common.py contains helper functions that could be used throughout m51 databot but don't deserve a separate file.
"""

import os


FIELD_KEYWORDS = ('跳高', '跳遠', '三級跳遠', '推鉛球', '擲壘球')
NAN_KEYWORDS = ('"缺"', '"無成績"', '"3"')
EVENT_MAPPING = {'女子丁組一百公尺': 'FDB', '女子丁組二百公尺': 'FDC', '女子丁組六十公尺': 'FDA', '女子丁組四百接力': 'FDS',
                 '女子丁組擲壘球': 'FDP', '女子丁組跳遠': 'FDM', '女子丁組跳高': 'FDL', '女子丙組一百公尺': 'FCB',
                 '女子丙組二百公尺': 'FCC', '女子丙組八百公尺': 'FCH', '女子丙組六十公尺': 'FCA', '女子丙組四百公尺': 'FCD',
                 '女子丙組四百接力': 'FCS', '女子丙組推鉛球': 'FCO', '女子丙組擲壘球': 'FCP', '女子丙組跳遠': 'FCM',
                 '女子丙組跳高': 'FCL', '女子乙組一百公尺': 'FBB', '女子乙組二百公尺': 'FBC', '女子乙組八百公尺': 'FBH',
                 '女子乙組千六接力': 'FBT', '女子乙組四百公尺': 'FBD', '女子乙組四百接力': 'FBS', '女子乙組推鉛球': 'FBO',
                 '女子乙組跳遠': 'FBM', '女子乙組跳高': 'FBL', '女子甲組一百公尺': 'FAB', '女子甲組二百公尺': 'FAC',
                 '女子甲組八百公尺': 'FAH', '女子甲組千六接力': 'FAT', '女子甲組四百公尺': 'FAD', '女子甲組四百接力': 'FAS',
                 '女子甲組推鉛球': 'FAO', '女子甲組跳遠': 'FAM', '女子甲組跳高': 'FAL', '師生歡樂跑': 'SAT', '測試項目': 'TOP',
                 '男子丁組一百公尺': 'MDB', '男子丁組二百公尺': 'MDC', '男子丁組六十公尺': 'MDA', '男子丁組四百接力': 'MDS',
                 '男子丁組擲壘球': 'MDP', '男子丁組跳遠': 'MDM', '男子丁組跳高': 'MDL', '男子丙組一百公尺': 'MCB',
                 '男子丙組二百公尺': 'MCC', '男子丙組八百公尺': 'MCH', '男子丙組六十公尺': 'MCA', '男子丙組四百公尺': 'MCD',
                 '男子丙組四百接力': 'MCS', '男子丙組推鉛球': 'MCO', '男子丙組跳遠': 'MCM', '男子丙組跳高': 'MCL',
                 '男子乙組一百公尺': 'MBB', '男子乙組三千公尺': 'MBJ', '男子乙組三級跳遠': 'MBN', '男子乙組二百公尺': 'MBC',
                 '男子乙組八百公尺': 'MBH', '男子乙組千五公尺': 'MBI', '男子乙組千六接力': 'MBT', '男子乙組四百公尺': 'MBD',
                 '男子乙組四百接力': 'MBS', '男子乙組推鉛球': 'MBO', '男子乙組跳遠': 'MBM', '男子乙組跳高': 'MBL',
                 '男子甲組一百公尺': 'MAB', '男子甲組三千公尺': 'MAJ', '男子甲組三級跳遠': 'MAN', '男子甲組二百公尺': 'MAC',
                 '男子甲組五千公尺': 'MAK', '男子甲組八百公尺': 'MAH', '男子甲組千五公尺': 'MAI', '男子甲組千六接力': 'MAT',
                 '男子甲組四百公尺': 'MAD', '男子甲組四百接力': 'MAS', '男子甲組推鉛球': 'MAO', '男子甲組跳遠': 'MAM',
                 '男子甲組跳高': 'MAL'
                 }
LEVEL_MAPPING = {'預賽': 'a', '初賽': 'b', '複賽': 'c', '決賽': 'd'}
CLASSES = {1: '信', 2: '望', 3: '愛', 4: '善', 5: '正', 6: '光'}
GRADES = {1: '初一', 2: '初二', 3: '初三', 4: '高一', 5: '高二', 6: '高三', 7: '小五', 8: '小六'}


def get_ext(filename: str) -> str:
    return os.path.splitext(filename)[1]


def is_field(comp: str) -> bool:
    for key in FIELD_KEYWORDS:
        if key in comp:
            return True
    return False
