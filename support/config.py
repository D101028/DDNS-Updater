import argparse
import json

from support.ip_fetcher import IpFetcher

parser = argparse.ArgumentParser(description="A simple tool for updating DDNS automatically.")
parser.add_argument("-c", "--config", type=str, help="Path to the configuration file")
args = parser.parse_args()

if args.config:
    config_path = args.config
else:
    config_path = "config.json"

with open(config_path, "r", encoding="utf8") as fp:
    data: dict = json.load(fp)

class Config:
    LOG_FOLDER: str = data.get("log-folder", "log-folder")

    CHECK_PERIOD: int = data.get("update-period", 30)

    IP_FETCHERS: list[IpFetcher] = [IpFetcher(i) for i in data.get("ip-fetchers", [{"type": "cmd-ip"}])]

    CHECK_LIST: list[dict] = data.get("check-list", [])
