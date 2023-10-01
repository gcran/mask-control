import time
import scripts
def security_mode(robot):
    
    #set to initial state
    robot.setStatusMsg('set to initial state')
    robot.setPersonality(robot.SLEEP)
    robot.setMotorCmd('head_yaw', robot.motors['head_yaw'].init_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1) or (abs(robot.motors['head_yaw'].getErr()) > 1) or (abs(robot.motors['eyes'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    time.sleep(2)
    
    #wake up
    robot.setStatusMsg('Wake Up')
    robot.setPersonality(robot.GOOD)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
    time.sleep(3)
    
    #play sound and change color
    robot.setStatusMsg('talk')
    robot.playSound('registering noise')
    scripts.lights_red(robot)
    time.sleep(robot.update_period)
    while (robot.isTalking()):
        time.sleep(robot.update_period)
        
    scripts.lights_red(robot)
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

    robot.setStatusMsg('sleep')
    robot.setPersonality(robot.SLEEP)
        
if (__name__ == '__main__'):   
    pass
