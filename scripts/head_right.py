import time
def head_right(robot):
    # head left
    robot.setStatusMsg('head right')
    robot.setMotorCmd('head_yaw', robot.motors['head_yaw'].ulim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['head_yaw'].getErr()) > 1)):
        time.sleep(robot.update_period)
