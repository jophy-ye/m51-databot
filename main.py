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

import settings
from blog import Blog, gen_blog
from db import db_results, db_promotion
from utils.common import *
from utils.FSDiff import FSDiff


# handle a single csv file given as a panda DataFrame
def handle_csv(df: pd.DataFrame, name: str) -> None:
    b = Blog(title=name, label=name[-2:])
    df = df.iloc[:-1, :]
    if df.iloc[0]['change_t'] != '"0"':
        db_results(df, name)

        df['change_t'].replace(NAN_KEYWORDS, np.NAN, inplace=True)
        df['dr'].replace('" "', '"?"', inplace=True)    # replace all those after 5 as ? (for sorting)
        # Note: same time/date/dist may lead to different rank. So first check dr
        df = df.sort_values(        # discarding the last row
            by=['dr', 'change_t'], na_position='last',
            ascending=[True, (not is_field(name))],
        )
        b.label += '成績'
        b.set_table(df.loc[:, ['sport_no', 'c_name', 'change_t']].to_numpy().tolist(),
                    df['rec_r'].to_numpy().tolist(), True)
    else:
        db_promotion(df, name)

        b.label += '名單'
        ev_l = LEVEL_MAPPING[name[-2:]]
        b.set_table(df.loc[:, ['sport_no', 'c_name', f'{ev_l}g', f'{ev_l}l']].to_numpy().tolist(),
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
            elif get_ext(filename) == '.html':
                handle_general(file.read(), name)
    gen_blog()


if __name__ == '__main__':
    try:
        settings.setup()
        main()
    except Exception as e:  # catch global error that haven't been caught by other means
        logging.fatal('Fatal (and Uncaught) Error occurred!', exc_info=True)
