# Domoticz Plugin for Philips ZhiRui E27 bulb aka Xiaomi Philips LED Ball Lamp


Domoticz Plugin for Philips ZhiRui E27 bulb aka Xiaomi Philips LED Ball Lamp

Fully base on : https://github.com/kofec/domoticz-AirPurifier

## Installation

* Make sure your Domoticz instance supports Domoticz Plugin System - see more https://www.domoticz.com/wiki/Using_Python_plugins
* __This version only for development branch of Domoticz__

Install Python-miio (Linux):
```
sudo pip3 install -U python-miio
```
Install Python-miio (Windows):
```
pip3 install -U python-miio
```

- Goes on your domoticz and clone this plugin
```
cd YOUR_DOMOTICZ_PATH/plugins

git clone https://github.com/deennoo/domoticz-Xiaomi-Led-Lamp.git
```
Give right to MyBulb.py (only in Linux)
```
sudo chmod 777 /home/pi/domoticz/plugins/domoticz-Xiaomi-Led-Lamp/MyBulb.py
```
and restart Domoticz (Linux):
```
sudo service domoticz.sh restart
```

* Go to Setup > Hardware and create new Hardware with type 'Xiaomi Philips LED Ball Lamp'
* Enter name (it's up to you), IP address and token

How to obtain token of your device please read this guide: https://python-miio.readthedocs.io/en/stable/discovery.html#tokens-from-backups

## Update
```
cd YOUR_DOMOTICZ_PATH/plugins/domoticz-Xiaomi-Led-Lamp
git pull
```
* Restart Domoticz


## Troubleshooting

In case of issues, mostly plugin not visible on plugin list, check logs if plugin system is working correctly.
You can visit Domoticz forum and ask your questions: https://www.domoticz.com/forum/viewtopic.php?f=65&t=25698

