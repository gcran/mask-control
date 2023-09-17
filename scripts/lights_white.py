def lights_white(robot):
    # eyes white
    robot.setStatusMsg('lights white')
       
    for i in robot.lights:
        robot.lights[i].setCmd(robot.lights[i].max_count, robot.lights[i].max_count, robot.lights[i].max_count)