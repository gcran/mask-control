import time
def eyes_center(robot):
    # eyes center
    robot.setStatusMsg('eyes center')
    robot.setMotorCmd('eyes', robot.motors['eyes'].init_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyes'].getErr()) > 1)):
        time.sleep(robot.update_period)
