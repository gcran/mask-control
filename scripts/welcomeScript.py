import time
import math
def welcomeScript(robot):
    
    #set to initial state
    print('set to initial state')
    robot.setPersonality(robot.GOOD)
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].llim_angle)
    robot.setMotorCmd('head_yaw', robot.motors['head_yaw'].init_angle)
    robot.setMotorCmd('eyes', robot.motors['eyes'].init_angle)
    robot.setLightCmd((robot.LIGHT_MIN, robot.LIGHT_MIN, robot.LIGHT_MIN))
    
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    time.sleep(1)
    
    #wake up
    print('wake up')
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].ulim_angle)
    robot.setLightCmd((robot.LIGHT_MIN, robot.LIGHT_MIN, robot.LIGHT_MIN))
    robot.setLightCmd((robot.LIGHT_MIN, robot.LIGHT_MAX, robot.LIGHT_MIN))
    
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
    time.sleep(1)
    
    #blink
    print('blink')
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].llim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].ulim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)): 
        time.sleep(robot.update_period)
        
    # eyes move left and at halfway point, trigger head yaw left
    print('eyes move left and at halfway point, trigger head yaw left')
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
    print('reverse back to start')
    robot.setMotorCmd('eyelids', robot.motors['eyes'].init_angle)
    robot.setMotorCmd('head_yaw', robot.motors['head_yaw'].init_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyes'].getErr()) > 1) or (abs(robot.motors['head_yaw'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    time.sleep(0.5)
        
    # eyes move right and at halfway point, trigger head yaw right
    print('eyes move right and at halfway point, trigger head yaw right')
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
    print('reverse back to start')
    robot.setMotorCmd('eyelids', robot.motors['eyes'].init_angle)
    robot.setMotorCmd('head_yaw', robot.motors['head_yaw'].init_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyes'].getErr()) > 1) or (abs(robot.motors['head_yaw'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    time.sleep(0.5)
    
    #blink
    print('blink')
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].llim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].ulim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    # talk
    print('talk')
    robot.playSound('welcome')
    time.sleep(robot.update_period)
    while (robot.isTalking()):
        mouth_command = ((robot.motors['mouth'].ulim_angle - robot.motors['mouth'].llim_angle)  * math.sin(time.time() % math.tau)) + (robot.motors['mouth'].llim_angle + (robot.motors['mouth'].ulim_angle - robot.motors['mouth'].llim_angle) / 2)
        robot.setMotorCmd('mouth', mouth_command)
        
    robot.playSound('all that is left')
    time.sleep(robot.update_period)
    while (robot.isTalking()):
        mouth_command = ((robot.motors['mouth'].ulim_angle - robot.motors['mouth'].llim_angle)  * math.sin(time.time() % math.tau)) + (robot.motors['mouth'].llim_angle + (robot.motors['mouth'].ulim_angle - robot.motors['mouth'].llim_angle) / 2)
        robot.setMotorCmd('mouth', mouth_command)
        
    #blink
    print('blink')
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].llim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].ulim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
if (__name__ == '__main__'):   
    from lib.janus import janus
    robot = janus('calibration.ini', test=False)
    welcomeScript(robot)
