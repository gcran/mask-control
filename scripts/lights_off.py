def lights_off(robot):
    # eyes closed
    robot.setStatusMsg('lights off')
       
    for i in robot.lights:
        robot.lights[i].setCmd(robot.lights[i].min_count, robot.lights[i].min_count, robot.lights[i].min_count)