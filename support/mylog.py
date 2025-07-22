import gzip
import os
import shutil
from datetime import datetime

from support.config import Config

IP_FILE = "last_ipv4.txt"
DIARY_FILE = "diary.log"
ERROR_FILE = "error.log"
MAX_LOG_SIZE = 5 * 1024 * 1024  # 5MB

def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

def save_ip(ipv4):
    with open(os.path.join(Config.LOG_FOLDER, IP_FILE), mode = "w") as file:
        file.write(ipv4)

def compress_log_file(log_path):
    if os.path.exists(log_path) and os.path.getsize(log_path) > MAX_LOG_SIZE:
        gz_path = log_path + "." + datetime.now().strftime("%Y%m%d%H%M%S") + ".gz"
        with open(log_path, "rb") as f_in, gzip.open(gz_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out) # type: ignore
        open(log_path, "w").close()  # Clear the original log file

def error_log(content):
    log_path = os.path.join(Config.LOG_FOLDER, ERROR_FILE)
    compress_log_file(log_path)
    with open(log_path, "a") as file:
        file.write(f"{get_timestamp()}: {content}\n")

def write_log(content):
    log_path = os.path.join(Config.LOG_FOLDER, DIARY_FILE)
    compress_log_file(log_path)
    with open(log_path, "a") as file:
        file.write(f"{get_timestamp()}: {content}\n")