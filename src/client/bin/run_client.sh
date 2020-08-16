#!/usr/bin/env bash

kill -9 $(ps aux | grep 'impersonator_client.py' | awk '{print $2}') 2> /dev/null

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
CONFIG=fomm/config/vox-adv-256.yaml
CKPT=weights/vox-adv-cpk.pth.tar

cd $DIR/..

python impersonator_client.py --config "$CONFIG" --checkpoint "$CKPT" --relative --adapt_scale --no-pad $@
