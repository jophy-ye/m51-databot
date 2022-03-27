"""
settings.py contains global settings for m51 databot, other files can include this file for project-wide settings.

A setup() is provided to configure m51 databot at the beginning of this program. This sets up logging, django and the
mysql client.
"""

import os
import json
import logging
import logging.config as log_config


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')       # where intermediate files for m51 databot is stored
SOURCE_DIR = os.path.join(BASE_DIR, 'sources')  # where csv files would be given
HTML_DIR = os.path.join(BASE_DIR, 'html')       # where the temporarily generated HTMLs go
FINAL_BLOG = os.path.join(DATA_DIR, 'liveblog.html')    # where the final generated HTML is, just a default value
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


def setup() -> None:
    with open('conf.json', 'r', encoding='utf-8') as file:
        conf_file = json.loads(file.read())
    global DEPLOY, HTML_DIR, FINAL_BLOG
    DEPLOY = conf_file.get('DEPLOY', False)
    if DEPLOY:
        FINAL_BLOG = os.path.join(BASE_DIR, '../../m51-docs/live_blog.html')

    if DEPLOY:
        LOGGING.update({
            'handlers': {
                'file_error': {
                    'level': 'INFO',
                    'class': 'logging.FileHandler',
                    'filename': os.path.join(BASE_DIR, '../../m51-docs/log.txt'),
                    'formatter': 'verbose',
                }
            },
            'loggers': {
                '': {
                    'handlers': ['file_error'],
                    'level': 'INFO',
                    'propagate': True,
                },
            },
        })
    log_config.dictConfig(LOGGING)

    import django
    from django.conf import settings
    settings.configure(TEMPLATES=[{
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(BASE_DIR, 'templates/'), ),
    }])
    django.setup()

    # TODO: configure db!!!

    logging.debug('Configuration finished.')
