import time
def eyes_open(robot):
    # eyes open
    robot.setStatusMsg('eyes open')
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].llim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
