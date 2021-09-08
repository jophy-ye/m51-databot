"""
main.py is the main entry of m51 databot. The main flow of the whole program is within this file too.
"""

import os
import logging

import settings


def main() -> None:
    pass


if __name__ == '__main__':
    try:
        settings.setup()
        main()
    except Exception as e:  # catch global error that haven't been caught by other means
        logging.exception(e)
