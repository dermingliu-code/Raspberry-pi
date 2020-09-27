kill -9 $(ps -eo pid,command | grep "47digitclock.py" | grep -v grep | awk '{print $1}')
python /home/pi/tm1637/tm1637-clear.py
