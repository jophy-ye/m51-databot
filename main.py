"""
main.py is the main entry of m51 databot. The main flow of the whole program is within this file too. This includes
fetching info from csv and compiling appropriate html files. In addition, it stores the contest results within our
mysql db.
"""

import os
import csv
import logging

import numpy as np
import pandas as pd
from pandas.errors import ParserError, EmptyDataError
import pymysql

import settings
from blog import Blog, gen_blog
from utils.common import *
from utils.FSDiff import FSDiff

SQL_INSERT = 'INSERT INTO score_table (athlete_num, game, change_t, rec_r, i_key) VALUES (%s, %s, %s, %s, %s)'


def into_db(df: pd.DataFrame, name: str, result_type: str) -> None:
    if not settings.DEPLOY:
        return
    event_id = EVENT_MAPPING[name[:-2]] + LEVEL_MAPPING[name[-2:]]
    # TODO: Support storing promotion info in db (when result_type is '名單')
    for r in range(len(df)):
        line = df.iloc[r]
        try:
            with settings.db.cursor() as cursor:
                cursor.execute(SQL_INSERT,
                               (line['sport_no'].strip('"'),
                                event_id,
                                str(line['change_t']).strip('"'),
                                line['rec_r'].strip('"'),
                                line['sport_no'].strip('"') + '_' + event_id))
        except pymysql.Error:
            logging.error('Error occurred when trying to write data into db', exc_info=True)


# handle a single csv file given as a panda DataFrame
def handle_csv(df: pd.DataFrame, name: str) -> None:
    b = Blog(title=name, label=name[-2:])
    if 'change_t' in df.columns:
        df['change_t'].replace(NAN_KEYWORDS, np.NAN, inplace=True)
        df = df.iloc[:-1, :].sort_values(       # discarding the last row
            by='change_t', na_position='last',
            ascending=(not is_field(name))
        )
        b.label += '成績'
        b.set_table(df.loc[:, ['sport_no', 'c_name', 'change_t']].to_numpy().tolist(),
                    df['rec_r'].to_numpy().tolist(), True)

        into_db(df, name, '成績')
    else:
        df = df.iloc[:-1, :]
        b.label += '名單'
        b.set_table(df.loc[:, ['sport_no', 'c_name']].to_numpy().tolist(),
                    None, False)
    b.compile()


# handle an HTML file and place it as an article
def handle_general(text: str, name: str) -> None:
    b = Blog(title=name, label='小道消息')
    b.set_html(text)
    b.compile()


def main() -> None:
    fs_watcher = FSDiff(settings.SOURCE_DIR)
    for (filename, version) in fs_watcher.file_change():
        name, ext = os.path.splitext(filename)
        if not ext:   # check if empty. Effectively ignore the dotfiles (.DS_Store, .gitignore, ...)
            continue
        logging.info(f'Handling "{filename}"')
        with open(os.path.join(settings.SOURCE_DIR, filename), 'r', encoding='big5', errors='replace') as file:
            if get_ext(filename) == '.csv':
                try:
                    df = pd.read_csv(file, quotechar='"', quoting=csv.QUOTE_NONE)
                    handle_csv(df, name)
                except (ParserError, EmptyDataError):
                    logging.error(f'Error occurred when parsing {filename}', exc_info=True)
                    continue
                except UnicodeDecodeError:
                    logging.error(f'Error occurred when decoding {filename}', exc_info=True)
                    continue
            else:
                handle_general(file.read(), name)
    gen_blog()


if __name__ == '__main__':
    try:
        settings.setup()
        main()
    except Exception as e:  # catch global error that haven't been caught by other means
        logging.fatal('Fatal (and Uncaught) Error occurred!', exc_info=True)
