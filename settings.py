"""
settings.py contains global settings for m51 databot, other files can include this file for project-wide settings.

A setup() is provided to configure m51 databot at the beginning of this program.
"""

import os
import json
import logging.config as log_config


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')       # where intermediate files for m51 databot is stored
SOURCE_DIR = os.path.join(BASE_DIR, 'sources')  # where csv files would be given
HTML_DIR = os.path.join(BASE_DIR, 'html')       # where the final generated HTML would go, just a default value
DEPLOY = False                                  # a default value in case setup() isn't run

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname}\t{asctime}\n{message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname}\n{message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stderr',
            'formatter': 'simple',
        },
    },
    'loggers': {
        '': {                               # default "root" logger
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

SELECTED_COL = ['sport_no', 'c_name', 'change_t']   # selected columns to be displayed on the website of m51


def setup() -> None:
    with open('conf.json', 'r', encoding='utf-8') as file:
        conf_file = json.loads(file.read())
    global DEPLOY, HTML_DIR
    DEPLOY = conf_file.get('DEPLOY')
    if DEPLOY:
        HTML_DIR = os.path.join(BASE_DIR, '../m51 docs/')

    if DEPLOY:
        LOGGING.update({
            'handlers': {
                'file_error': {
                    'level': 'ERROR',
                    'class': 'logging.FileHandler',
                    'filename': os.path.join(BASE_DIR, ''),
                    'formatter': 'verbose',
                }
            },
            'loggers': {
                '': {
                    'handlers': ['file_error'],
                    'level': 'WARNING',
                    'propagate': True,
                },
            },
        })
    log_config.dictConfig(LOGGING)
    # TODO: configure db!!!
