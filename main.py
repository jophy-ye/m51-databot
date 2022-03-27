"""
main.py is the main entry of m51 databot. The main flow of the whole program is within this file too.
"""

import os
import csv
import logging

import numpy as np
import pandas as pd
from pandas.errors import ParserError, EmptyDataError

import settings
from blog import Blog, gen_blog
from utils.common import *
from utils.FSDiff import FSDiff


# handle a single csv file given as a panda DataFrame
def handle_csv(df: pd.DataFrame, name: str) -> None:
    df['change_t'].replace(NAN_KEYWORDS, np.NAN, inplace=True)
    df = df.iloc[:-1, :].sort_values(       # discarding the last row
        by='change_t', na_position='last',
        ascending=(not is_field(name))
    )
    # A little trick is used here, the last four characters of name is exactly the type (Ofc in normal conditions)
    b = Blog(title=name, label=name[-4:])
    b.set_table(df.loc[:, ['sport_no', 'c_name', 'change_t']].to_numpy().tolist(),
                df['rec_r'].to_numpy().tolist())
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
        if not ext:     # check if empty. Effectively ignore the dotfiles (.DS_Store, .gitignore, ...)
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
