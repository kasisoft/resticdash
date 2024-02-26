#!/bin/bash

if [ "$(whoami)" != "root" ]; then
    echo "You need to run this script as root !"
    exit 1
fi

export DIRNAME=$(readlink -f $(dirname .))

mkdir -p /opt/resticdash /etc/resticdash

cp -rp "${DIRNAME}/static" "${DIRNAME}/resticdash.pex" /opt/resticdash
cp "${DIRNAME}/resticdash.yaml" /etc/resticdash
chmod +x /opt/resticdash/resticdash.pex

mv "${DIRNAME}/resticdash.service" /etc/systemd/system

echo "ResticDash has been installed to /opt/resticdash"
echo "Configure your backups in /etc/resticdash/resticdash.json"

echo "A service resticdash.service has been installed (/etc/systemd/system/resticdash.service)"
echo "You need to enable it after it has been configured using the following steps:"
echo ""
echo "systemctl enable resticdash.service"
echo "systemctl daemon-reload"
