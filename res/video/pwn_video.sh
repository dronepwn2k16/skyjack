#!/bin/sh

SP=$(ps|grep "[r]espawner"|awk '{print $1}')
kill -9 $SP

ELF=$(ps|grep "program.elf"|awk '{print $1}')
kill -9 $ELF

sleep 2
chmod +x /data/video/pwn_video
/data/video/pwn_video
