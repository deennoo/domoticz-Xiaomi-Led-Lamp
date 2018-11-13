# domoticz-Xiaomi-Led-Lamp
Domoticz Plugin for Philips ZhiRui E27 bulb aka Xiaomi Philips LED Ball Lamp

base on : https://github.com/kofec/domoticz-AirPurifier

ONLY TESTED ON LINUX


1 - install Python-miio 

pip3 install -U python-miio


Then goes on your domoticz and clone this plugin

cd YOUR_DOMOTICZ_PATH/plugins
git clone https://github.com/deennoo/domoticz-Xiaomi-Led-Lamp.git



next evolution : 

Use native CCCW widget
Use set_brightness_and_color_temperature(brightness, cct) = Set brightness level and the correlated color temperature. instead of 2 different command
