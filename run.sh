#!/bin/bash

#set -euo pipefail

export KEY=$(curl -sf http://localhost:8006/cdh/resource/default/key/secretkey)

python3 search.py /mnt/df_enc.csv "$DESCRIPTION"

sleep infinity
