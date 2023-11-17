import time
import scripts
def slow_scan(robot):
    robot.setStatusMsg('Scanning')
    robot.motors['head_yaw'].setRate(60)
    scripts.eyes_open(robot)
    scripts.lights_red(robot)
    scripts.head_center(robot)
    time.sleep(1)
    scripts.head_left(robot)
    time.sleep(1)
    scripts.head_center(robot)
    time.sleep(1)
    scripts.head_right(robot)
    time.sleep(1)
    scripts.head_center(robot)
    time.sleep(1)
    scripts.head_left(robot)
    time.sleep(1)
    scripts.head_center(robot)
    time.sleep(1)
    scripts.head_right(robot)
    time.sleep(1)
    scripts.head_center(robot)
    time.sleep(1)
    robot.setPersonality(robot.SLEEP)
        
if (__name__ == '__main__'):   
    pass
