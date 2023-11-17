#!./.venv/bin/python

import RPi.GPIO as GPIO
from lib.janus import janus
import scripts
from mfrc522 import SimpleMFRC522
import paho.mqtt.client as paho

    # remote control button mapping
btn_lookup = {'Button 1': scripts.head_left,
                'Button 2': scripts.head_center,
                'Button 3': scripts.head_right,
                '2774745088': scripts.eyes_half_open,
                '74090265': scripts.welcome_demo,
                '76765212': scripts.security_mode,
                '1648833105': scripts.slow_scan,
                '83267831': scripts.welcomeScript}

def on_message(mosq, obj, msg):
    cmd = msg.payload.decode('utf-8')
    if cmd in btn_lookup.keys():
        btn_lookup[cmd](bot)

    else:
        bot.setStatusMsg('No Script match found for input ' + cmd)
    
    mosq.publish('pong', 'ack', 0)


if __name__ == "__main__":
    #tag lookup table. Tag ID: script
    tag_lookup = {712803352631: scripts.blink,
                  2774745088: scripts.security_mode}
    


    bot = janus('calibration.ini', test=True)
    reader = SimpleMFRC522()
    mqtt_client = paho.Client()
    mqtt_client.on_message = on_message
    mqtt_client.connect("127.0.0.1", 1883, 60)
    mqtt_client.subscribe("remote/command", 0)

    id = ''
    text = ''

    try:
        while(True):
            id, text = reader.read_no_block()
            if id != '':
                if id in tag_lookup.keys():
                    tag_lookup[id](bot)
                    id = ''
            else:
                bot.setStatusMsg('No Script match found for tag.')
                id = ''
                
            mqtt_client.loop()
    finally:
        GPIO.cleanup()
        bot.deinit()
