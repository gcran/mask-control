def lights_red(robot):
    # eyes red
    robot.setStatusMsg('lights red')
       
    for i in robot.lights:
        robot.lights[i].setCmd(robot.lights[i].max_count, robot.lights[i].min_count, robot.lights[i].min_count)