# Domoticz Plugin for Philips ZhiRui E27 bulb aka Xiaomi Philips LED Ball Lamp


Domoticz Plugin for Philips ZhiRui E27 bulb aka Xiaomi Philips LED Ball Lamp

Fully base on : https://github.com/kofec/domoticz-AirPurifier

ONLY TESTED ON LINUX


- Install Python-miio 
```
sudo pip3 install -U python-miio
```

- Goes on your domoticz and clone this plugin
```
cd YOUR_DOMOTICZ_PATH/plugins

git clone https://github.com/deennoo/domoticz-Xiaomi-Led-Lamp.git
```
Give right to MyBulb.py
```
sudo chmod 777 /home/pi/domoticz/plugins/domoticz-Xiaomi-Led-Lamp/MyBulb.py
```
and restart Domoticz
```
sudo service domoticz.sh restart
```

- Next evolution : 

Use Domoticz native CCCW widget

Use set_brightness_and_color_temperature(brightness, cct) = Set brightness level and the correlated color temperature. instead of 2 different command



