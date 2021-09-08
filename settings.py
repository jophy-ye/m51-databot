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
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, ''),
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'm51': {
            'handlers': ['file_error'],
            'level': 'WARNING',
            'propagate': True
        }
    }
}


def setup() -> None:
    with open('conf.json', 'r', encoding='utf-8') as file:
        conf_file = json.loads(file.read())
    global DEPLOY, HTML_DIR
    DEPLOY = conf_file.get('DEPLOY')
    if DEPLOY:
        HTML_DIR = os.path.join(BASE_DIR, '../m51 docs/')
        log_config.dictConfig(LOGGING)
    # TODO: configure db!!!
