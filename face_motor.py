class face_motor():
    """Class for a servo in the robot face."""
    def __init__(self, pca, params):
        self.pca = pca
        self.channel = int(params['channel'], 10)
        self.llim_angle = int(params['llim_angle'], 10)
        self.ulim_angle = int(params['ulim_angle'], 10)
        self.period = float(params['pwm_period'])
        self.fsr = 0xFFFF
        self.min_count = round((float(params['min_pulse']) / self.period) * self.fsr)
        self.max_count = round((float(params['max_pulse']) / self.period) * self.fsr)
        self.angle2count = (self.max_count - self.min_count) / int(params['range'], 10)

        self.max_step_angle = int(params['maxstep'], 10)
        self.max_step_count = round(self.max_step_angle * self.angle2count)

        self.init_angle = int(params['init'], 10)
        self.err = 0
        self.setCmd(self.init_angle)
        self.out_count = self.cmd_count

    def setCmd(self, cmd):
        self.cmd_count = round(self.angle2count * max(self.llim_angle, min(self.ulim_angle, cmd)) + self.min_count)
        
    def setRate(self, rate):
        self.max_step_angle = rate
        self.max_step_count = round(self.max_step_angle * self.angle2count)

    def update(self):
        self.err = self.cmd_count - self.out_count
        if (self.err > 0):
            self.out_count = self.out_count + min(self.max_step_count, self.err)
        else:
            self.out_count = self.out_count + max(-self.max_step_count, self.err)

        self.pca.channels[self.channel].duty_cycle = self.out_count

    def getCmd(self):
        return self.out_count

    def getOutput(self):
        return self.out_count

    def getErr(self):
        return self.err
    
    def getRate(self):
        return self.max_step_angle

