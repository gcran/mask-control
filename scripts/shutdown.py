def shutdown(robot: janus):
    
    #zero out all motors and lights
    for i in robot.motors:
        robot.motors[i].pca.channels[robot.motors[i].channel].duty_cycle = 0
        
    for i in robot.lights:
        robot.lights[i].setCmd(0, 0, 0)
        
if (__name__ == '__main__'):   
    from lib.janus import janus
    robot = janus('calibration.ini', test=False)
    shutdown(robot)
