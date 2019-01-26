# A Python plugin for Domoticz to access Xiaomi Philips LED Ball Lamp
#
# Author: Deennoo
#
# TODO: Update text sensors only when changed
#
#
# v0.1.0 - initial version,
# fetching data Xiaomi Philips LED Ball Lamp print(MyBulb.status()) "<PhilipsBulbStatus power=on, brightness=9, color_temperature=9, scene=0, delay_off_countdown=0>"

# v0.1.1 - Add Scenes control
# v0.1.2 - remove on/off switch, bright dimmer, temp dimmer, to use a cccw widget, update only if needed, sperate scenes widget status / !!! still segfault @ plugin restart
"""
<plugin key="XiaomiPhilipsLEDBallLamp" name="Xiaomi Philips LED Ball Lamp" author="Deennoo" version="0.1.2" wikilink="https://github.com/rytilahti/python-miio" externallink="https://github.com/deennoo/domoticz-Xiaomi-Led-Lamp/tree/master">
    <params>
		<param field="Address" label="IP Address" width="200px" required="true" default="127.0.0.1"/>
		<param field="Mode1" label="Xiaomi Philips LED Ball Lamp token" default="" width="400px" required="true"  />
        <param field="Mode3" label="Check every x minutes" width="40px" default="1" required="true" />
		<param field="Mode6" label="Debug" width="75px">
			<options>
				<option label="True" value="Debug"/>
				<option label="False" value="Normal" default="true" />
			</options>
		</param>
    </params>
</plugin>
"""
import Domoticz
import json
import sys
import datetime
import socket
import subprocess
import site

class UnauthorizedException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class SensorNotFoundException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

class ConnectionErrorException(Exception):
    def __init__(self, expression, message):
        self.expression = expression
        self.message = message

# temporery class

class BulbStatus:
    """Container for status reports from the Xiaomi Philips Bulb."""

    def __init__(self, AddressIP, Mode1):
        """
        Response of script:

		   "<PhilipsBulbStatus power=on, brightness=9, color_temperature=9, scene=0, delay_off_countdown=0>"
        """

        addressIP = str(AddressIP)
        Mode1 = str(Mode1)
        data = subprocess.check_output(['bash', '-c', './MyBulb.py ' + addressIP + ' ' + Mode1], cwd=Parameters["HomeFolder"])
        data = str(data.decode('utf-8'))
        if Parameters["Mode6"] == 'Debug':
            Domoticz.Debug(data[:30] + " .... " + data[-30:])
        data = data[19:-2]
        data = data.replace(' ', '')
        data = dict(item.split("=") for item in data.split(","))
        self.brightness = data["brightness"]
        self.color_temperature = data["color_temperature"]
        self.power = data["power"]
        self.scene = data["scene"]
        for item in data.keys():
            Domoticz.Debug(str(item) + " => " + str(data[item]))

class BasePlugin:
    enabled = False

    def __init__(self):
        # Consts
        self.version = "0.1.2"

        self.EXCEPTIONS = {
            "SENSOR_NOT_FOUND":     1,
            "UNAUTHORIZED":         2,
        }

        self.debug = False
        self.inProgress = False

        # Do not change below UNIT constants!
        self.UNIT_SCENES         = 1
        self.UNIT_CCCW           = 2		

        self.nextpoll = datetime.datetime.now()
        return


    def onStart(self):
        Domoticz.Debug("onStart called")
        if Parameters["Mode6"] == 'Debug':
            self.debug = True
            Domoticz.Debugging(1)
            DumpConfigToLog()
        else:
            Domoticz.Debugging(0)

        Domoticz.Heartbeat(20)
        self.pollinterval = int(Parameters["Mode3"]) * 60


        
        #create switches
        if (len(Devices) == 0):

            Options = {"Scenes": "|||||", "LevelNames": "Off|Bright|TV|Warm|Midnight", "LevelOffHidden": "true", "SelectorStyle": "0"}
            Domoticz.Device(Name="Scenes", Unit=self.UNIT_SCENES, Type=244, Subtype=62 , Switchtype=18, Options = Options).Create()
            Domoticz.Device(Name="CCCW", Unit=self.UNIT_CCCW, Type=241, Subtype=8, Switchtype=7).Create()
			
			
            Domoticz.Log("Devices created.")
        else:

		#Scenes		
            if (self.UNIT_SCENES in Devices ):
                Domoticz.Log("Device UNIT_SCENES with id " + str(self.UNIT_SCENES) + " exist")
				
            else:
               Options = {"Scenes": "|||||", "LevelNames": "Off|Bright|TV|Warm|Midnight", "LevelOffHidden": "true", "SelectorStyle": "0"}
               Domoticz.Device(Name="Scenes", Unit=self.UNIT_SCENES, Type=244, Subtype=62 , Switchtype=18, Options = Options).Create()				
         #CCCW
            if (self.UNIT_CCCW in Devices ):
                Domoticz.Log("Device UNIT_CCCW with id " + str(self.UNIT_CCCW) + " exist")
				
            else:
               Domoticz.Device(Name="CCCW", Unit=self.UNIT_SCENES, Type=241, Subtype=8 , Switchtype=7).Create()	
            

        self.onHeartbeat(fetch=False)

    def onStop(self):
        Domoticz.Log("onStop called")
        Domoticz.Debugging(0)

    def onConnect(self, Status, Description):
        Domoticz.Log("onConnect called")

    def onMessage(self, Data, Status, Extra):
        Domoticz.Log("onMessage called")

    def onCommand(self, Unit, Command, Level, Color):
        Domoticz.Log(
            "onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level)+ "', Color: " + str(Color))

        # Parameters["Address"] - IP address, Parameters["Token"] - token
        commandToCall = './MyBulb.py ' + Parameters["Address"] + ' ' + Parameters["Mode1"] + ' '
     
		
		#widget selector scenes	
        if Unit == self.UNIT_SCENES:
            commandToCall += '--scene=' + str(int(int(Level)/10))
		
		#widget cccw	
        elif Unit == self.UNIT_CCCW:
         
		#OFF
         if Command == "Off" :
                  commandToCall += '--power=' + str(Command).upper()
		#ON
         elif Command == "On" :
                  commandToCall += '--power=' + str(Command).upper()
		
		#Set Level
         elif Command =="Set Level" :
            commandToCall += '--level=' + str(int(int(Level)))
		
		#White Temp & Brightness
         elif Command == "Set Color" :
          Hue_List = json.loads(Color)		 
          if Hue_List['m'] == 2:            
           Temp = 100-((100*Hue_List['t'])/255);
           commandToCall += '--brightemp=' + str(int(int(Level))) + ','+ str(int(int(Temp)))
        
        else:
            Domoticz.Log("onCommand called not found")

        if Parameters["Mode6"] == 'Debug':
            Domoticz.Debug("Call command: " + commandToCall)
        data = subprocess.check_output(['bash', '-c', commandToCall], cwd=Parameters["HomeFolder"])
        data = str(data.decode('utf-8'))
        if Parameters["Mode6"] == 'Debug':
            Domoticz.Debug(data)
        self.onHeartbeat(fetch=True)
		
    

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(
            Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self):
        Domoticz.Log("onDisconnect called")

    def postponeNextPool(self, seconds=3600):
        self.nextpoll = (datetime.datetime.now() + datetime.timedelta(seconds=seconds))
        return self.nextpoll

    def createDevice(self, key=None):
        """create Domoticz virtual device"""

        def createSingleDevice(key):
            """inner helper function to handle device creation"""

            item = self.variables[key]
            _unit = key
            _name = item['Name']

            # skip if already exists
            if key in Devices:
                Domoticz.Debug(_("Device Unit=%(Unit)d; Name='%(Name)s' already exists") % {'Unit': key, 'Name': _name})
                return

            try:
                _options = item['Options']
            except KeyError:
                _options = {}

            _typename = item['TypeName']

            try:
                _used = item['Used']
            except KeyError:
                _used = 0

            try:
                _image = item['Image']
            except KeyError:
                _image = 0

            Domoticz.Debug(_("Creating device Name=%(Name)s; Unit=%(Unit)d; ; TypeName=%(TypeName)s; Used=%(Used)d") % {
                               'Name':     _name,
                               'Unit':     _unit,
                               'TypeName': _typename,
                               'Used':     _used,
                           })

            Domoticz.Device(
                Name=_name,
                Unit=_unit,
                TypeName=_typename,
                Image=_image,
                Options=_options,
                Used=_used
            ).Create()

        if key:
            createSingleDevice(key)
        else:
            for k in self.variables.keys():
                createSingleDevice(k)


    def onHeartbeat(self, fetch=False):
        Domoticz.Debug("onHeartbeat called")
        now = datetime.datetime.now()

        if fetch == False:
            if self.inProgress or (now < self.nextpoll):
                 Domoticz.Debug("Awaiting next pool: %s" % str(self.nextpoll))
                 return

        # Set next pool time
        self.postponeNextPool(seconds=self.pollinterval)

        try:
            # check if another thread is not running
            # and time between last fetch has elapsed
            self.inProgress = True

            res = self.sensor_measurement(Parameters["Address"], Parameters["Mode1"])
				
            try:
                if res.power == "on":                    
                   if res.scene == "0":
                    UpdateDevice(self.UNIT_SCENES, 0, str(int(res.scene)*10))
                    UpdateDevice(self.UNIT_CCCW, 1, str(int(res.brightness)))
                   else:
                    UpdateDevice(self.UNIT_SCENES, 1, str(int(res.scene)*10))
                    UpdateDevice(self.UNIT_CCCW, 1, str(int(res.brightness)))
					
                elif res.power == "off":
                    UpdateDevice(self.UNIT_CCCW, 0, str(int(res.brightness)))
                    UpdateDevice(self.UNIT_SCENES, 0, str(int(res.scene)*10))
            except KeyError:
                pass  # No power value

            self.doUpdate()
        except Exception as e:
            Domoticz.Error("Unrecognized error: %s" % str(e))
        finally:
            self.inProgress = False
        if Parameters["Mode6"] == 'Debug':
            Domoticz.Debug("onHeartbeat finished")
        return True


    def doUpdate(self):
        Domoticz.Log(("Starting device update"))

    def sensor_measurement(self, addressIP, Mode1):
        """current sensor measurements"""
        return BulbStatus(addressIP, Mode1)



global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Status, Description):
    global _plugin
    _plugin.onConnect(Status, Description)

def onMessage(Data, Status, Extra):
    global _plugin
    _plugin.onMessage(Data, Status, Extra)

def onCommand(Unit, Command, Level, Color):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Color)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect():
    global _plugin
    _plugin.onDisconnect()

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return

def UpdateDevice(Unit, nValue, sValue):
    # Make sure that the Domoticz device still exists (they can be deleted) before updating it
    if (Unit in Devices):
        if (Devices[Unit].nValue != nValue) or (Devices[Unit].sValue != sValue):
            Devices[Unit].Update(nValue=nValue, sValue=str(sValue))
            Domoticz.Log("Update " + str(nValue) + ":'" + str(sValue) + "' (" + Devices[Unit].Name + ")")
    return
