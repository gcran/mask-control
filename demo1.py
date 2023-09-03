#!/usr/bin/python

from janus import janus
import time

bot = janus('calibration.ini')
bot.setMotorCmd('eyes', bot.motors['eyes'].llim_angle)
bot.setMotorCmd('head_yaw', bot.motors['head_yaw'].llim_angle)
bot.setPersonality(bot.GOOD)
time.sleep(bot.update_period*2)
while((abs(bot.motors['head_yaw'].getErr()) > 1) or (abs(bot.motors['eyes'].getErr()) > 1) or (abs(bot.motors['head_roll'].getErr()) > 1)):
    time.sleep(bot.update_period)
    

bot.playSound('c-3po')


time.sleep(6)
bot.setPersonality(bot.EVIL)
bot.setMotorCmd('eyes', bot.motors['eyes'].ulim_angle)
bot.setMotorCmd('head_yaw', bot.motors['head_yaw'].ulim_angle)
time.sleep(bot.update_period*2)
while((abs(bot.motors['head_yaw'].getErr()) > 1) or (abs(bot.motors['eyes'].getErr()) > 1) or (abs(bot.motors['head_roll'].getErr()) > 1)):
    time.sleep(bot.update_period)
    
bot.playSound('bmsma')
time.sleep(6)
