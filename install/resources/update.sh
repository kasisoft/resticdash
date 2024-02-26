#!/bin/bash

if [ "$(whoami)" != "root" ]; then
    echo "You need to run this script as root !"
    exit 1
fi

export DIRNAME=$(readlink -f $(dirname .))


echo "Stopping service..."
service resticdash stop

mkdir -p /opt/resticdash /etc/resticdash

cp -rp "${DIRNAME}/static" "${DIRNAME}/resticdash.pex" /opt/resticdash
chmod +x /opt/resticdash/resticdash.pex

echo "Restarting service..."
service resticdash start

echo "Update completed"
