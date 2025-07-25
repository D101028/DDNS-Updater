# DDNS-Updater
A simple tool for updating DDNS automatically.

## Setup
Make sure you have installed the python environment (>= 3.10 recommanded). 

1. Clone this repo. 
    ```bash
    git clone https://github.com/D101028/DDNS-Updater.git
    cd DDNS-Updater
    ```

2. Create and activate virtual environment. 
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```

3. Install packages.
    ```bash
    pip install -r requirements.txt
    ```

4. Run setup.sh
    ```bash
    chmod +x ./setup.sh
    sudo /path/to/this/setup.sh
    ```

More about the usage of this tool, checkout `python3 main.py -h`

## Config
Example of `config.json`:
```json
{
    "log-folder": "./log", 
    "check-period": 30, 
    "ip-fetchers": [
        {
            "type": "cmd-ip", 
            "network-card-name": "ppp0"
        }, 
        {
            "type": "net-access", 
            "url": "https://api.ipify.org/"
        }
    ], 
    "check-list": [
        {
            "type": "access-url", 
            "url": "https://your-ddns-update-url"
        }, 
        {
            "type": "cloudflare", 
            "zone-id": "your-cf-servername-zone-id", 
            "record-id": "your-cf-servername-record-id", 
            "api-token": "your-cf-servername-api-token", 
            "record-name": "your.record.name", 
            "record-type": "A"
        }
    ]
}
```

- Available ipfetchers
    - `cmd-ip`: Get the IP by command line tool /bin/ip with a given nerwork card name. 
    - `net-access`: Get the IP by accessing a ip checkout website.

- Supported DDNS service
    - `access-url`: All DDNS services whose updating service supports url accessing. 
    - `cloudflare`: Cloudflare DDNS update. 
