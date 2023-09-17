import time
def head_left(robot):
    # head left
    robot.setStatusMsg('head left')
    robot.setMotorCmd('head_yaw', robot.motors['head_yaw'].llim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['head_yaw'].getErr()) > 1)):
        time.sleep(robot.update_period)
