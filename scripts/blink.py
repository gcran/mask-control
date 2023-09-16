    
import time
def blink(robot):
    # eyes closed
    robot.setStatusMsg('blink')
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].llim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)

    # eyes open
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].ulim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)): 
        time.sleep(robot.update_period)