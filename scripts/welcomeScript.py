import time
import math
def welcomeScript(robot):
    
    #set to initial state
    robot.setStatusMsg('set to initial state')
    robot.setPersonality(robot.SLEEP)
    robot.setMotorCmd('head_yaw', robot.motors['head_yaw'].init_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1) or (abs(robot.motors['head_yaw'].getErr()) > 1) or (abs(robot.motors['eyes'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    time.sleep(2)
    
    #wake up
    robot.setPersonality(robot.SECURITY)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
    time.sleep(1)
    
    #blink
    robot.setStatusMsg('blink')
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].llim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].ulim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)): 
        time.sleep(robot.update_period)
        
    # talk
    robot.setStatusMsg( 'talk')
    robot.playSound('c-3po')
    time.sleep(robot.update_period)
    while (robot.isTalking()):
        time.sleep(robot.update_period)
    
    time.sleep(1)
    #blink
    robot.setStatusMsg('flip head')
    robot.setPersonality(robot.FRIENDLY)
    time.sleep(robot.update_period)
    while((abs(robot.motors['head_roll'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
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
    
    #blink
    robot.setStatusMsg('blink')
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].llim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    robot.setMotorCmd('eyelids', robot.motors['eyelids'].ulim_angle)
    time.sleep(robot.update_period)
    while((abs(robot.motors['eyelids'].getErr()) > 1)):
        time.sleep(robot.update_period)
        
    # talk
    robot.setStatusMsg('talk')
    robot.playSound('welcome')
    time.sleep(robot.update_period)
    while (robot.isTalking()):
        time.sleep(robot.update_period)
        
    robot.playSound('all that is left')
    time.sleep(robot.update_period)
    while (robot.isTalking()):
        time.sleep(robot.update_period)
        
    #blink
    robot.setStatusMsg('blink')
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
