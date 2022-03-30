"""
medals.py is a standalone script (aside from the flow of the whole project) that gets the num of medals
for each class, storing the data in a json file. The data is categorized by the events.
"""

import os
import csv
import json
import logging

import pandas as pd
from pandas.errors import ParserError, EmptyDataError

import settings
from utils.common import *


data = {}


# add a medal for the student with a given event_name. Results are stored in data
def add_medal(class_name: str, event_name: str, rank: int) -> None:
    assert len(class_name) == 3
    # for that whole class the num of total medals
    data.setdefault(class_name, {'medals_total': 0, 'records_total': 0})
    # for that event and class the num of total medals
    data[class_name].setdefault(event_name, 0)
    data[class_name].setdefault(rank, 0)
    
    data[class_name]['medals_total'] += 1
    data[class_name][event_name] += 1
    data[class_name][rank] += 1     # gold, silver, bronze


def write_json() -> None:
    if settings.DEPLOY:
        json_path = '../../m51-docs/dashboard/m51_medals.json'
    else:
        json_path = 'data/m51_medals.json'
    with open(os.path.join(settings.BASE_DIR, json_path), 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False)
    

# ordering of classes based on their num of medals
def sort_key(class_info) -> bool:
    return data[class_info].get(1, 0) * 1e6 + data[class_info].get(2, 0) * 1e3 + data[class_info].get(3, 0)


def main():
    article_list = os.listdir(settings.SOURCE_DIR)

    for filename in article_list:
        name, ext = os.path.splitext(filename)
        if ext != '.csv':
            continue
        with open(os.path.join(settings.SOURCE_DIR, filename), 'r', encoding='big5', errors='replace') as file:
            try:
                df = pd.read_csv(file, quotechar='"', quoting=csv.QUOTE_NONE)
                if df.iloc[0]['change_t'] == '"0"':     # just a promotion list
                    continue

                # rank, medals
                if name[-2:] == '決賽':
                    for rank in range(1, 4):
                        row = df.loc[df['dr'] == f'"{rank}"'].iloc[0]
                        sport_no = row['sport_no'].strip('"')
                        if sport_no.isnumeric():    # not a relay contest
                            class_name = GRADES[int(sport_no[0])] + CLASSES[int(sport_no[1])]
                            add_medal(class_name, name[4:-2], rank)
                        else:
                            add_medal(row['c_name'].strip('"')[:3], name[4:-2], rank)
                    
                # records count
                df_rec = df.loc[df['rec_r'].str.contains('\*') == True]     # '\' used to escape reg exp
                for r in range(len(df_rec)):
                    row = df_rec.iloc[r]
                    sport_no = row['sport_no'].strip('"')
                    if sport_no.isnumeric():
                        class_name = GRADES[int(sport_no[0])] + CLASSES[int(sport_no[1])]
                    else:
                        class_name = row['c_name'].strip('"')[:3]
                    data[class_name]['records_total'] += 1
            except (ParserError, EmptyDataError):
                logging.error(f'Medals: Error occurred when parsing {filename}', exc_info=True)
                continue

    classes = sorted(data.keys(), key=sort_key, reverse=True)
    for c in range(len(classes)):
        data[classes[c]]['order'] = c + 1
    write_json()


if __name__ == '__main__':
    try:
        settings.setup()
        main()
    except Exception as e:  # catch global error that haven't been caught by other means
        logging.fatal('Fatal (and Uncaught) Error occurred!', exc_info=True)
