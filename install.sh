#!/bin/sh
if [ ! -d "~/.switch2gp" ]
then
    echo "Already installed?"
    echo "Run purge.sh to remove old versions."
    exit 1
else
    mkdir "~/.switch2gp"
    cp "switch2gp/*" "~/.switch2gp"
    sudo apt install python3 python3-pip
    pip3 install python-twitter wget
    cd "~/.switch2gp"
    ./app/gphotos-uploader-cli init
    nano t.py
    nano ~/.gphotos-uploader-cli/config.hjson
    ./app/gphotos-uploader-cli auth
    mkdir media/Switch #because git doesn't copy empty folders
fi
