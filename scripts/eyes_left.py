import time
def eyes_left(robot):
    # eyes left
    robot.setStatusMsg('eyes left')
    robot.setMotorCmd('eyes', robot.motors['eyes'].ulim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyes'].getErr()) > 1)):
        time.sleep(robot.update_period)
