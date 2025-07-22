import logging
import os
import time

from support.config import Config
from support.mylog import IP_FILE, DIARY_FILE, ERROR_FILE
from support.updater import Updater

def init_data():
    if not os.path.isdir(Config.LOG_FOLDER):
        os.mkdir(Config.LOG_FOLDER)
    for file in (IP_FILE, DIARY_FILE, ERROR_FILE):
        path = os.path.join(Config.LOG_FOLDER, file)
        if not os.path.isfile(path):
            with open(path, "w") as fp:
                fp.write("")

if __name__ == "__main__":
    init_data()
    time.sleep(5)
    updater = Updater()
    logging.info(">> Updater Started <<")
    updater.run()
