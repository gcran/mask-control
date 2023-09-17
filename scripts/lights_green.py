def lights_green(robot):
    # eyes green
    robot.setStatusMsg('lights green')
       
    for i in robot.lights:
        robot.lights[i].setCmd(robot.lights[i].min_count, robot.lights[i].max_count, robot.lights[i].min_count)