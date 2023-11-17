import time
import scripts

def welcome_demo(robot):
    robot.setPersonality(robot.FRIENDLY)
    time.sleep(robot.update_period)
    while((abs(robot.motors['head_roll'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    robot.playSound('welcome')
    while (robot.isTalking()):
        time.sleep(robot.update_period)
    
    robot.setPersonality(robot.SECURITY)
    time.sleep(robot.update_period)
    while((abs(robot.motors['head_roll'].getErr()) > 1)):
        time.sleep(robot.update_period)
    
    scripts.eyes_half_open(robot)
    time.sleep(1)
    robot.playSound('registering noise')
    while (robot.isTalking()):
        time.sleep(robot.update_period)
        
    scripts.eyes_left(robot)
    time.sleep(1)
    scripts.eyes_right(robot)
    time.sleep(1)
    scripts.eyes_center(robot)
    time.sleep(1)
    scripts.blink(robot)
    time.sleep(1)
    robot.setPersonality(robot.FRIENDLY)
    time.sleep(1)
    scripts.blink(robot)
    time.sleep(1)
    robot.playSound('all that is left')
    while (robot.isTalking()):
        time.sleep(robot.update_period)



if (__name__ == '__main__'):   
    from lib.janus import janus
    robot = janus('calibration.ini', test=False)
    welcome_demo(robot)
