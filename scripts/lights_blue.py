def lights_blue(robot):
    # eyes blue
    robot.setStatusMsg('lights blue')
       
    for i in robot.lights:
        robot.lights[i].setCmd(robot.lights[i].min_count, robot.lights[i].min_count, robot.lights[i].max_count)