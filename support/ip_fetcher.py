import subprocess

import requests

def get_ip_by_cmd(name: str):
    process = subprocess.Popen(
        ["/bin/ip", "a"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        return None
    
    # resolve ip from ppp0 information
    result = stdout.decode().strip()
    for line in result.splitlines():
        if name in line:
            # Found the ppp0 interface section, now look for the inet line(s)
            idx = result.splitlines().index(line)
            for subline in result.splitlines()[idx+1:]:
                if "inet " in subline and name in subline:
                    # Extract the IP address before the slash
                    ip = subline.strip().split()[1].split('/')[0]
                    return ip
                if subline and not subline.startswith(' '):
                    # Reached next interface
                    break
            else:
                return None
    else:
        return None

def get_ip_by_net(url: str):
    try:
        process = subprocess.Popen(
                    ["wget", "-qO-", "-4", url],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE
                )
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return stdout.decode().strip()
    except:
        pass 
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return 

class IpFetcher:
    def __init__(self, conf: dict):
        self.type_ = conf.get("type", "cmd-ip")
        if self.type_ == "cmd-ip":
            self.network_card_name = conf.get("network-card-name", "ppp0")
        elif self.type_ == "net-access":
            self.url = conf.get("url", "https://api.ipify.org/")
        else:
            raise ValueError(f"Unknown IpFetcher type: `{self.type_}`")

    def fetch_ip(self):
        if self.type_ == "cmd-ip":
            ip = get_ip_by_cmd(self.network_card_name)
            return ip
        elif self.type_ == "net-access":
            ip = get_ip_by_net(self.url)
            return ip
