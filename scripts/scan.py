import time
def scan(robot):
    # eyes move left and at halfway point, trigger head yaw left
    robot.setStatusMsg('eyes move left and at halfway point, trigger head yaw left')
    robot.setMotorCmd('eyes', (robot.motors['eyes'].llim_angle + robot.motors['eyes'].init_angle) / 2)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyes'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    robot.setMotorCmd('eyes', robot.motors['eyes'].llim_angle)
    robot.setMotorCmd('head_yaw', robot.motors['head_yaw'].llim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyes'].getErr()) > 1) or (abs(robot.motors['head_yaw'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    time.sleep(0.5)
    
    # reverse back to start
    robot.setStatusMsg('reverse back to start')
    robot.setMotorCmd('eyes', robot.motors['eyes'].init_angle)
    robot.setMotorCmd('head_yaw', robot.motors['head_yaw'].init_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyes'].getErr()) > 1) or (abs(robot.motors['head_yaw'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    time.sleep(0.5)
        
    # eyes move right and at halfway point, trigger head yaw right
    robot.setStatusMsg('eyes move right and at halfway point, trigger head yaw right')
    robot.setMotorCmd('eyes', (robot.motors['eyes'].ulim_angle + robot.motors['eyes'].init_angle) / 2)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyes'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    robot.setMotorCmd('eyes', robot.motors['eyes'].ulim_angle)
    robot.setMotorCmd('head_yaw', robot.motors['head_yaw'].ulim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyes'].getErr()) > 1) or (abs(robot.motors['head_yaw'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    time.sleep(0.5)
    
    # reverse back to start
    robot.setStatusMsg('reverse back to start')
    robot.setMotorCmd('eyes', robot.motors['eyes'].init_angle)
    robot.setMotorCmd('head_yaw', robot.motors['head_yaw'].init_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyes'].getErr()) > 1) or (abs(robot.motors['head_yaw'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    time.sleep(0.5)