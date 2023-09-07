class rgb_led_control():
    def __init__(self, pca, params):
        self.pca = pca
        self.channel = {'r': int(params['rchannel'], 10), 'g': int(params['gchannel'], 10), 'b': int(params['bchannel'], 10)}
        
        # cross fade rate in seconds
        self.max_count = 65535
        self.min_count = 0
        self.rate = float(params['rate'])
        self.update_period = float(params['update_period'])
        self.rate_count = round(self.max_count / max(self.update_period, self.rate))
        
        self.cmd = {'r': int(params['r_init'], 16), 'g': int(params['g_init'], 16), 'b': int(params['b_init'], 16)}
        self.err = {'r': 0, 'g': 0, 'b': 0}
        self.out = {'r': self.cmd['r'], 'g': self.cmd['g'], 'b': self.cmd['b']}
        self.setCmd(self.cmd['r'], self.cmd['g'], self.cmd['b'])
        
    def setCmd(self, rcmd, gcmd, bcmd):     
        
        self.cmd['r'] = rcmd
        self.cmd['g'] = gcmd
        self.cmd['b'] = bcmd
        
    def setRate(self, rate):
        self.rate = rate
        self.rate_count = round(self.max_count / max(self.update_period, self.rate))
        
    def getOut(self):
        return (self.out['r'], self.out['g'], self.out['b'])
    
    def update(self, time):
        self.max_step_count = round((self.rate_count * time))
        for i in ['r', 'g', 'b']:
            self.err[i] = self.cmd[i] - self.out[i]
            if (self.err[i] > 0):
                self.out[i] = min(self.max_count, self.out[i] + min(self.max_step_count, self.err[i]))
            else:
                self.out[i] = max(self.min_count, self.out[i] + max(-self.max_step_count, self.err[i]))
                
            self.pca.channels[self.channel[i]].duty_cycle = self.out[i]
