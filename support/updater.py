import json
import logging
import os
import time

import requests
from requests import HTTPError

from support.config import Config
from support.mylog import IP_FILE, write_log, save_ip, error_log

def is_ip_changed(ipv4):
    with open(os.path.join(Config.LOG_FOLDER, IP_FILE), mode = "r") as file:
        previous_ipv4 = file.read()
    return previous_ipv4 != ipv4

def fetch_url(url) -> tuple[bool, str]:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return False, response.text
    except HTTPError as e:
        return True, f"{e}: {response.text}"
    except Exception as e:
        return True, f"Error: {e}"

def cloudflare_update(zone_id, 
                      record_id, 
                      api_token, 
                      record_name, 
                      record_type, 
                      ip) -> tuple[bool, str]:
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    dns_record = {
        "type": record_type,
        "name": record_name,
        "content": ip,
        "ttl": 120, 
        "proxied": True
    }

    try:
        r = requests.put(
            f"https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records/{record_id}",
            headers=headers,
            data=json.dumps(dns_record)
        )
        r.raise_for_status()
        return False, r.text
    except HTTPError as e:
        return True, f"{e}: {r.text}"
    except Exception as e:
        return True, f"Error: {e}"

class Updater:
    def __init__(self):
        self.ipv4 = None

    def update_ddns(self) -> bool:
        all_passed = True
        check_list = Config.CHECK_LIST
        for item in check_list:
            type_ = item.get("type")
            if type_ == "access-url":
                status, resp = fetch_url(item.get("url"))
                if status == 1:
                    error_log(resp)
                    all_passed = False
                else:
                    write_log(f"DDNS update: {self.ipv4}")
            elif type_ == "cloudflare":
                zone_id = item.get("zone-id")
                record_id = item.get("record-id")
                api_token = item.get("api-token")
                record_name = item.get("record-name")
                record_type = item.get("record-type")
                status, text = cloudflare_update(zone_id, record_id, api_token, record_name, record_type, self.ipv4)
                if status:
                    error_log(text)
                    all_passed = False
                else:
                    write_log(f"Cloudflare DDNS update: {self.ipv4}")
        return all_passed

    def check_ddns(self):
        for fetcher in Config.IP_FETCHERS:
            self.ipv4 = fetcher.fetch_ip()
            if self.ipv4 is None:
                write_log("Error: ip fetcher failed")
                continue
            if is_ip_changed(self.ipv4):
                logging.info(f"Try to update ddns ip: {self.ipv4}")
                all_passed = self.update_ddns()
                if all_passed:
                    save_ip(self.ipv4)
            else:
                print("pass")
            break

    def run(self):
        while True:
            self.check_ddns()
            time.sleep(Config.CHECK_PERIOD)

