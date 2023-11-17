import time
def eyes_closed(robot):
    # eyes closed
    robot.setStatusMsg('eyes closed')
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].ulim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
