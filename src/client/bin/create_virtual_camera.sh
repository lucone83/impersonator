#!/usr/bin/env bash

CAMID_VIRT=9
FILE=/dev/video$CAMID_VIRT

if [[ ! -w "$FILE" ]]; then
    echo "Creating virtual camera $FILE (sudo privelege required)"
    sudo apt-get install -y v4l2loopback-dkms
    sudo modprobe v4l2loopback exclusive_caps=1 video_nr=$CAMID_VIRT card_label="impersonator"
fi
