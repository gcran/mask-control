import time
def head_center(robot):
    # head center
    robot.setStatusMsg('head center')
    robot.setMotorCmd('head_yaw', robot.motors['head_yaw'].init_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['head_yaw'].getErr()) > 1)):
        time.sleep(robot.update_period)
