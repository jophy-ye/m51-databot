"""
db.py contains functions which can store contest results in mysql. Input is generally expected to be given as a
dataframe.
"""

import logging

import pandas as pd
import pymysql

import settings
from utils.common import *


SQL_RES = 'REPLACE INTO score_table (athlete_num, game, change_t, dr, rec_r, i_key) VALUES (%s, %s, %s, %s, %s, %s)'
SQL_PRO = 'REPLACE INTO athletes_info (athlete_num, game, in_final, `order`, i_key) VALUES (%s, %s, %s, %s, %s)'


def db_results(df: pd.DataFrame, name: str) -> None:
    if not settings.DEPLOY:
        return
    event_id = EVENT_MAPPING[name[:-2]] + LEVEL_MAPPING[name[-2:]]
    for r in range(len(df)):
        line = df.iloc[r]
        try:
            with settings.db.cursor() as cursor:
                cursor.execute(SQL_RES,
                               (line['sport_no'].strip('"'),
                                event_id,
                                str(line['change_t']).strip('"'),
                                line['dr'].strip('"'),
                                line['rec_r'].strip('"'),
                                line['sport_no'].strip('"') + '_' + event_id))
        except pymysql.Error:
            logging.error('Error occurred when trying to write data into db (result)', exc_info=True)


def db_promotion(df: pd.DataFrame, name: str) -> None:
    if not settings.DEPLOY:
        return
    event_id = EVENT_MAPPING[name[:-2]] + LEVEL_MAPPING[name[-2:]]
    for r in range(len(df)):
        line = df.iloc[r]
        try:
            with settings.db.cursor() as cursor:
                cursor.execute(SQL_PRO,
                               (line['sport_no'].strip('"'),
                                EVENT_MAPPING[name[:-2]],
                                LEVEL_MAPPING[name[-2:]],
                                f'{line["dg"]}組{line["dl"]}線',
                                line['sport_no'].strip('"') + '_' + event_id))
        except pymysql.Error:
            logging.error('Error occurred when trying to write data into db (promotion)', exc_info=True)
