import time
import scripts

def welcome_demo(robot):
    scripts.eyes_open(robot)
    robot.playSound('welcome')
    robot.setPersonality(robot.SECURITY)
    time.sleep(2)
    scripts.eyes_half_open(robot)
    scripts.eyes_left(robot)
    scripts.eyes_right(robot)
    scripts.blink(robot)
    robot.setPersonality(robot.FRIENDLY)
    scripts.blink(robot)
    scripts.eyes_left(robot)
    scripts.eyes_right(robot)



if (__name__ == '__main__'):   
    from lib.janus import janus
    robot = janus('calibration.ini', test=False)
    welcome_demo(robot)