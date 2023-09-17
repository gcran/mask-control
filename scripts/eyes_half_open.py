import time
def eyes_half_open(robot):
    # eyes half closed
    robot.setStatusMsg('eyes half open')
    robot.setMotorCmd('eyelids', (robot.motors['eyelids'].llim_angle + robot.motors['eyelids'].ulim_angle) / 2)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
