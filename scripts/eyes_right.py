import time
def eyes_right(robot):
    # eyes right
    robot.setStatusMsg('eyes right')
    robot.setMotorCmd('eyes', robot.motors['eyes'].llim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyes'].getErr()) > 1)):
        time.sleep(robot.update_period)
