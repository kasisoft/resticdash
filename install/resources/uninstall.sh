#!/bin/bash

if [ "$(whoami)" != "root" ]; then
    echo "You need to run this script as root !"
    exit 1
fi

export DIRNAME=$(readlink -f $(dirname .))

systemctl disable resticdash.service
systemctl daemon-reload

rm -rf /etc/resticdash /opt/resticdash
