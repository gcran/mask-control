#!./.venv/bin/python

import RPi.GPIO as GPIO
from lib.janus import janus
import scripts
from mfrc522 import SimpleMFRC522

#tag lookup table. Tag ID: script
tag_lookup = {712803352631: scripts.blink,
              422390288647: scripts.security_mode}


bot = janus('calibration.ini', test=True)
reader = SimpleMFRC522()
try:
        id, text = reader.read()
        if id in tag_lookup.keys():
            tag_lookup[id](bot)
        else:
            bot.setStatusMsg('No Script match found for tag.')
        

finally:
        GPIO.cleanup()
        bot.deinit()
