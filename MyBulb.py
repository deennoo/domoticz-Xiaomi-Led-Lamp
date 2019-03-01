#!/usr/bin/python3

import sys
import argparse
import site
path=''
path=site.getsitepackages()
for i in path:
    sys.path.append(i)

import miio.philips_bulb

parser = argparse.ArgumentParser(description='Script which comunicate with PhilipsBulb.')
parser.add_argument('IPaddress', help='IP address of PhilipsBulb' )
parser.add_argument('token', help='token to login to device')
parser.add_argument('--level', type=int, choices=range(1, 100), help='choose level')
parser.add_argument('--temp', type=int, choices=range(1, 100), help='choose White Temp')
parser.add_argument('--power', choices=['ON', 'OFF'], help='power ON/OFF')
parser.add_argument('--debug', action='store_true', help='if define more output is printed')
parser.add_argument('--scene', type=int, choices=range(1, 5), help='choose scene')
# --brightemp = set_brightness_and_color_temperature()
parser.add_argument('--brightemp', type=str, help='choose Brightness and White Temp')

args = parser.parse_args()
if args.debug:
    print(args)
MyBulb = miio.philips_bulb.PhilipsBulb(args.IPaddress, args.token)

if args.level:
	MyBulb.set_brightness(args.level)

if args.temp:
	MyBulb.set_color_temperature(args.temp)

if args.brightemp:
    #print(args.brightemp)
    brightness = args.brightemp[:args.brightemp.find(",")]
    #print("brightness is " + brightness)
    cct = args.brightemp[args.brightemp.find(",") + 1 :]
    #print("cct is " + cct)
    MyBulb.set_brightness_and_color_temperature(int(brightness), int(cct))

if args.scene:
	MyBulb.set_scene(args.scene)

if args.power:
    if args.power == "ON":
        MyBulb.on()
    elif args.power == "OFF":
        MyBulb.off()

print(MyBulb.status())
