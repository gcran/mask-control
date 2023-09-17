import time
def head_tilt_45(robot):
    # head tilt 45 degrees
    robot.setStatusMsg('45 degree head tilt')
    if robot.getPersonality() == robot.EVIL:
        robot.setMotorCmd('head_roll', robot.motors['head_roll'].ulim_angle - 45)
    else:
        robot.setMotorCmd('head_roll', robot.motors['head_roll'].llim_angle + 45)
    time.sleep(robot.update_period)
    while((abs(robot.motors['head_roll'].getErr()) > 1)):
        time.sleep(robot.update_period)
