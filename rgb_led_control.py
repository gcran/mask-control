class rgb_led_control():
    def __init__(self, pca, params):
        self.pca = pca
        self.channel = {'r': int(params['rchannel'], 10), 'g': int(params['gchannel'], 10), 'b': int(params['bchannel'], 10)}
        self.maxstep = 0x0700
        
        self.cmd = {'r': 0, 'g': 0, 'b': 0}
        self.err = {'r': 0, 'g': 0, 'b': 0}
        self.out = {'r': 0, 'g': 0, 'b': 0}
        self.setCmd(self.cmd['r'], self.cmd['g'], self.cmd['b'])
        
    def setCmd(self, rcmd, gcmd, bcmd):     
        
        self.cmd['r'] = rcmd
        self.cmd['g'] = gcmd
        self.cmd['b'] = bcmd
        
    def update(self):
        for i in ['r', 'g', 'b']:
            self.err[i] = self.cmd[i] - self.out[i]
            if (self.err[i] > 0):
                self.out[i] = self.out[i] + min(self.maxstep, self.err)
            else:
                self.out[i] = self.out[i] + max(-self.maxstep, self.err)
                
            self.pca.channels[self.channel[i]].duty_cycle = self.out[i]
