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
        self.angle2countslope = (self.max_count - self.min_count) / int(params['range'], 10)
        self.angleoffset = int(params['center_angle'], 10) - int(params['range'], 10)/2

        self.rate = int(params['rate'], 10)

        self.init_angle = int(params['init'], 10)
        self.err = 0
        self.setCmd(self.init_angle)
        self.out_count = self.cmd_count

    def angle2count(self, angle):
        return self.angle2countslope * (angle - self.angleoffset) + self.min_count

    def count2angle(self, count):
        return (count / self.angle2countslope)  + self.angleoffset

    def setCmd(self, cmd):
        self.cmd_count = round(self.angle2count(max(self.llim_angle, min(self.ulim_angle, cmd))))
        
        
    def setRate(self, rate):
        self.rate = rate

    def update(self):
        self.err = self.cmd_count - self.out_count
        # self.max_step_count = round((self.rate * time) * self.angle2count)
        if (self.err > 0):
            self.out_count = min(self.max_count, max(self.min_count, self.cmd_count))
        else:
            self.out_count = max(self.min_count, min(self.max_count, self.cmd_count))

        self.pca.channels[self.channel].duty_cycle = self.out_count

    def getCmd(self):
        return self.count2angle(self.cmd_count)

    def getOutput(self):
        return self.count2angle(self.out_count)

    def getErr(self):
        return self.count2angle(self.err)
    
    def getRate(self):
        return self.rate

