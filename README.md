# unifi-video-mqtt-py

Inspired by (and forked from) https://github.com/mzac/unifi-video-mqtt

# Introduction
This script can run on your Unifi Video server and push MQTT messages to an MQTT broker when motion is detected.

This can be useful for systems like Homeassistant that are lacking motion detection integration with Unifi Video.

# Reference
Unifi Video writes to */var/log/unifi-video/motion.log* and it ouputs logs like this.  This script parses this log:
```
1559209064.179 2019-05-30 19:07:44.179/ACST: INFO   [uv.analytics.motion] [AnalyticsService] [REDACTED|Front Door] MotionEvent type:start event:17 clock:14369834 in AnalyticsEvtBus-0
1559209090.983 2019-05-30 19:08:10.983/ACST: INFO   [uv.analytics.motion] [AnalyticsService] [REDACTED|Front Door] MotionEvent type:stop event:17 clock:14396566 in AnalyticsEvtBus-1
```

# TODO
* setup to run as a service/daemon

# Requirements
* Unifi Video Server
* MQTT Client
* MQTT Server
* Python 3
* mqtt-paho python library

# Optional
* mqtt client tools on UniFi Server

# KNOWN ISSUES

There is a bug with the parsing of the log where spaces exist in the camera name. I've mitigated this for my use-case of "Front Porch" in the IF statement at line 48. I'll need to spend more time on this to figure out a better way to split the log rows into a dict/tuple.


# IMPORTANT!!!
Before starting the service, make sure to edit `UnifiVideoMQTT.py` with your specific
settings:

MQTT_BASE_TOPIC = 'camera/motion'
MQTT_BROKER = "192.168.x.x"
LOGPATH = "/var/log/unifi-video/motion.log"
MQTT_PORT = 1883

Test it to make sure it works:
```
/usr/local/bin/UnifiVideoMQTT.py
```

Create some motion on your camera and subscribe to your MQTT server and see if you see motion:

```
root@pi3:~# mosquitto_sub -h 192.168.x.x -t "camera/motion/#" -v
camera/motion/front_door on
camera/motion/front_door off
