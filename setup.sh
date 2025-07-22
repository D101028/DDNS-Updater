#!/bin/bash
set -e

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root (use sudo)"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CURRENT_USER=$(logname)

# Register systemd
echo "Register systemd service..."
cat <<EOF | tee /etc/systemd/system/ddns-updater.service > /dev/null
[Unit]
Description=DDNS Updater
After=network.target

[Service]
Type=simple
ExecStart=/bin/sh -c "/bin/sleep 10 && python3 main.py"
WorkingDirectory=$SCRIPT_DIR
Restart=always
User=$CURRENT_USER
Environment="PATH=$SCRIPT_DIR/.venv/bin"

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable ddns-updater
systemctl start ddns-updater

echo "Complete."
echo "Use \`systemctl status ddns-updater\` to check the updater."
exit 0